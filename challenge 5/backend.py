import numpy as np
from vertexai.language_models import TextEmbeddingModel
from sklearn.metrics.pairwise import cosine_similarity
from google.cloud import bigquery
from fastapi import FastAPI, Body
from settings import get_settings, DEFAULT_SYSTEM_PROMPT
from pydantic import BaseModel
from typing import Optional

from google.genai import Client
from google.genai.types import Part

settings = get_settings()
app = FastAPI(title="ADS Online Agent")

# === Define request/response models ===
class SimpleChatRequest(BaseModel):
    text: str

class ChatResponse(BaseModel):
    response: str
    error: Optional[str] = None

# === Initialize external clients ===
bq_client = bigquery.Client()
embedding_model = TextEmbeddingModel.from_pretrained("text-embedding-005")

GENAI_CLIENT = Client(
    location=settings.VERTEXAI_LOCATION, 
    project=settings.VERTEXAI_PROJECT_ID,    
    vertexai=True,
)

GEMINI_MODEL_NAME = "gemini-2.0-flash-001"

# GEMINI_MODEL_NAME = "publishers/google/models/gemini-1.5-pro-preview-0409"

# === Helper function: BigQuery similarity-based FAQ retrieval ===
def get_context_from_bigquery(user_input: str, top_k: int = 3) -> str:
    query = """
    SELECT question, answer, ml_generate_embedding_result
    FROM `ADSFaq.ads_faq_embedded`
    """
    df = bq_client.query(query).to_dataframe()
    df["embedding_vector"] = df["ml_generate_embedding_result"].apply(lambda x: np.array(x, dtype=np.float32))

    user_vector = embedding_model.get_embeddings([user_input])[0].values
    user_vector = np.array(user_vector, dtype=np.float32).reshape(1, -1)

    similarities = cosine_similarity(user_vector, df["embedding_vector"].tolist())[0]
    df["score"] = similarities

    top = df.sort_values("score", ascending=False).head(top_k)
    return "\n".join([f"Q: {row.question}\nA: {row.answer}" for _, row in top.iterrows()])

# === Chat endpoint ===
@app.post("/chat", response_model=ChatResponse)
async def chat(request: SimpleChatRequest = Body(...)) -> ChatResponse:
    print(request)
    try:
        context = get_context_from_bigquery(request.text)
        print(context)
        if not context:
            context = "No relevant information found."

        prompt = f"Context:\n{context}\n\nQuestion:\n{request.text}"

        chat_model = GENAI_CLIENT.chats.create(
            model=GEMINI_MODEL_NAME,
            history=[],
            config={"system_instruction": "You are a helpful FAQ Assistant. Respond only to the question."}
        )

        response = chat_model.send_message(prompt)

        # ✅ Safely extract text from the Gemini response

        model_reply = (
            response.candidates[0].content.parts[0].text
            if response and response.candidates
            else "No response received."
        )

        return ChatResponse(response=model_reply)

    except Exception as e:
        return ChatResponse(response="", error=f"Error in generating response: {str(e)}")

# === Local run ===
if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(app, host="0.0.0.0", port=8081)
