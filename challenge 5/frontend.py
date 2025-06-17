import gradio as gr
import requests
from settings import get_settings

settings = get_settings()


def get_response_from_llm_backend(message: str, history) -> str:
    payload = {
        "text": message if message.strip() else " ",
    }

    try:
        response = requests.post(settings.BACKEND_URL, json=payload)
        response.raise_for_status()
        result = response.json()

        # ✅ Only return error if it's a non-empty string
        error = result.get("error")
        if error:
            return f"Error: {error}"

        return result.get("response", "No response received from backend")
    except requests.exceptions.RequestException as e:
        return f"Error connecting to backend: {str(e)}"


if __name__ == "__main__":
    demo = gr.ChatInterface(
        fn=get_response_from_llm_backend,
        title="ADS Online Agent",
        description="Chat with a Gemini-powered ADS Online Agent assistant.",
        textbox=gr.Textbox(placeholder="Ask something...", lines=1),
    )

    demo.launch(server_name="0.0.0.0", server_port=8080)
