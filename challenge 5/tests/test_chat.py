import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend import app  #


import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock


client = TestClient(app)

test_cases = [
    {
        "question": "When was the Alaska Department of Snow established?",
        "context": "Q: When was the Alaska Department of Snow established?\nA: The Alaska Department of Snow (ADS) was established in 1959, coinciding with Alaska’s admission as a U.S. state.",
        "expected": "1959"
    },
    {
        "question": "do they have mobile app ?",
        "context": "Q: do they have mobile app ?\nA: Yes. The ADS “SnowLine” app offers real-time plow tracking, road conditions, and the ability to submit service requests directly from your phone.",
        "expected": "SnowLine app offers real-time"
    },
    {
        "question": "ok, When was Aurora Bay founded?",
        "context": "",  # No relevant context
        "expected": "cannot be answered"
    },
    {
        "question": "who is CFO ?",
        "context": "Q: who is CFO ?\nA: The current CFO is Janet Kirk, appointed in 2022.",
        "expected": "Janet Kirk"
    }
]

@pytest.mark.parametrize("case", test_cases)
@patch("main.get_context_from_bigquery")
@patch("main.GENAI_CLIENT")
def test_chat_endpoint(mock_genai_client, mock_get_context, case):
    mock_get_context.return_value = case["context"]

    # Mock Gemini response
    mock_chat = MagicMock()
    mock_response = MagicMock()
    mock_response.candidates = [MagicMock(content=MagicMock(parts=[MagicMock(text=case["expected"])]))]
    mock_chat.send_message.return_value = mock_response
    mock_genai_client.chats.create.return_value = mock_chat

    response = client.post("/chat", json={"text": case["question"]})
    assert response.status_code == 200
    result = response.json()

    assert "error" not in result or result["error"] is None
    assert case["expected"][:10] in result["response"]  # Partial check for stability
