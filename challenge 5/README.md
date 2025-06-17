# ADS Online Agent – Proof of Concept

![Screenshot of ADS Online Agent](./39785da4-930e-4298-8e18-5ce9bbf9727a.png)

## 🔍 Overview

This project is a **Generative AI-powered chatbot** developed as a proof of concept (POC) for the **Alaska Department of Snow (ADS)**. It is designed to help alleviate call center volume by answering common resident questions through a web-based interface.

**Hosted URL:** [https://ads-agent-748152039909.us-central1.run.app/](https://ads-agent-748152039909.us-central1.run.app/)

---

## ✅ Objectives Met

- ✅ Built and deployed a chatbot capable of handling text queries related to ADS and Aurora Bay.
- ✅ Integrated with **Gemini Pro** for generating intelligent responses.
- ✅ Implemented **Retrieval-Augmented Generation (RAG)** using a backend data store (BigQuery vector embeddings).
- ✅ Provided **API access** to backend functionality via a FastAPI interface.
- ✅ Designed **unit tests** to validate message classification and backend responses.
- ✅ Incorporated **Google Model Evaluation API** (stubbed or integrated depending on access).
- ✅ Applied **prompt filtering and response validation** to ensure safe and accurate outputs.
- ✅ Frontend developed with **Gradio**, allowing interactive chat experiences via web.

---

## 🧱 Architecture

### Components

- **Frontend:** Gradio-based chat UI
- **Backend:** FastAPI server
- **Model:** Gemini 2.0 Flash (via Google Vertex AI)
- **RAG Store:** BigQuery with `ml_generate_embedding_result`
- **Deployment:** Cloud Run (GCP)

### Data Flow

1. **User** enters query via Gradio.
2. **Frontend** sends POST to FastAPI backend.
3. **Backend**:
   - Filters prompt
   - Embeds query
   - Retrieves top matches from BigQuery
   - Constructs final prompt with context
   - Sends to Gemini model
4. **Gemini** returns response, which is sent back to frontend.
5. **User** sees response in chat.

---

## 🔐 Security & Privacy Considerations

- ✅ **Input sanitization** applied at backend
- ✅ **Prompt filters** to block disallowed topics (e.g., food-related queries)
- ✅ HTTPS endpoint hosted via **Cloud Run**
- ✅ No personally identifiable information (PII) is collected or stored

---

## 📏 Accuracy & Evaluation

- Leveraged **Google Evaluation API** for prototype-level evaluation
- Limited to known context (e.g., department info, FAQ database)
- Includes fallback for unsupported or unanswerable queries

---

## 🧪 Testing

- Unit tests created using `pytest`
- Tests include:
  - Prompt classification
  - RAG retrieval quality
  - API route validation

---

## 🚀 Deployment

- Deployed to **Cloud Run**:
  - Region: `us-central1`
  - Memory Optimized: Yes (512 MiB+)
- Gemini model served via `Vertex AI`
- Configured with secure environment variables for API keys and project ID

---

## 📸 Screenshot

![Screenshot](./39785da4-930e-4298-8e18-5ce9bbf9727a.png)

---

## 💬 Contact

For demo access or questions, please contact the AI Engineering team.

## Project Setup

<img src="https://avatars2.githubusercontent.com/u/2810941?v=3&s=96" alt="Google Cloud Platform logo" title="Google Cloud Platform" align="right" height="96" width="96"/>

# Simple application to interact with Gemini API

"Python: Gemini API" is a simple sample application that shows you how to interact with Google's Gemini APIs .

## Table of Contents

- [Directory contents](#directory-contents)
- [Setting up the API Key](#setting-up-the-api-key)
- [Getting started](#getting-started-with-vs-code)
- [Sign up for user research](#sign-up-for-user-research)

## Directory contents

- `launch.json` - config file for later when you deploy your application to Google Cloud
- `main.py` - the Python sample application that asks Gemini API to generate content based on a prompt
- `requirements.txt` - includes the google generative ai dependency

## Setting up the API Key

Before you can use the Gemini API, you must first obtain an API key. If you don't already have one, create a key with one click in Google AI Studio.
[Get API](https://makersuite.google.com/app/apikey)

## Getting started with Cloud Code

### Run the application locally

1. Make sure you have generated the API key as shown above. Please make sure to use and store this key securely.

1. Install the package using
   `pip install -r requirements.txt`

1. Run this using
   `python main.py`

### Documentation

1. You can see detailed API Reference for the Gemini APIs [here](https://googledevai.google.com/api)

1. You can see more samples and things to do [here](https://googledevai.google.com/tutorials/python_quickstart)

### Other things to try

1. If you're new to Google Cloud, [create an account](https://console.cloud.google.com/freetrial/signup/tos) to evaluate how our products perform in real-world scenarios. New customers also get $300 in free credits to run, test, and deploy workloads.

1. Install the Cloud Code [VS Code plugin](https://cloud.google.com/code/docs/vscode/install#installing) or [Jetbrains Extension](https://cloud.google.com/code/docs/intellij/install) if you haven't already.

1. Access Cloud Code [documentation](https://cloud.google.com/code/docs/) to learn how you can deploy your app to Google Cloud

### Sign up for user research

We want to hear your feedback!

The Cloud Code team is inviting our user community to sign-up to participate in Google User Experience Research.

If you’re invited to join a study, you may try out a new product or tell us what you think about the products you use every day. At this time, Google is only sending invitations for upcoming remote studies. Once a study is complete, you’ll receive a token of thanks for your participation such as a gift card or some Google swag.

[Sign up using this link](https://google.qualtrics.com/jfe/form/SV_4Me7SiMewdvVYhL?reserved=1&utm_source=In-product&Q_Language=en&utm_medium=own_prd&utm_campaign=Q1&productTag=clou&campaignDate=January2021&referral_code=UXbT481079) and answer a few questions about yourself, as this will help our research team match you to studies that are a great fit.
