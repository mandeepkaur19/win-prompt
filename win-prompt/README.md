# 🔍 TruthLens: AI-Powered Misinformation Detection

[![Deployed on Cloud Run](https://img.shields.io/badge/Deployed-Google_Cloud_Run-blue?logo=googlecloud)](YOUR_CLOUD_RUN_URL_HERE)
[![Firebase Hosting](https://img.shields.io/badge/Hosted-Firebase-orange?logo=firebase)](YOUR_FIREBASE_URL_HERE)

> **Hackathon Submission Note:** You can test the live application here: **[(Cloud Run URL) Your Link Here]**

TruthLens is a deterministic, highly-scalable fact-checking engine built to process messy, real-world inputs (like WhatsApp forward screenshots or text claims) and evaluate them strictly against live Google Search data to minimize LLM hallucination.

## 🏗 The 3-Layer Architecture
We engineered TruthLens specifically to separate the "thinking" (Orchestration) from the "doing" (Execution) to guarantee accuracy and modularity.

1. **Layer 1: The Directive** 
   - A strict SOP detailing how the AI must behave, how to detect partial truths, and how to format outputs without conversational noise.
2. **Layer 2: Orchestration (FastAPI)**
   - A lightweight `api.py` router that manages the state flow: *Ingest -> Extract -> Search -> Generate Verdict -> Format*. 
3. **Layer 3: execution (`/execution`)**
   - **`image_to_text_extractor.py`**: Uses Gemini Vision to clean text from noisy WhatsApp/Meme images.
   - **`claim_analyzer.py`**: Uses Gemini *Structured Outputs* to deterministically extract verifiable claims.
   - **`fact_check_retriever.py`**: Queries the Google Custom Search API for real-time, real-world context.
   - **`truth_score_generator.py`**: Binds the Gemini evaluator *strictly* to the retrieved context to output a JSON Verdict (Score, Fact Checks, Confidence).

## 🚀 Key Features
- **Zero Hallucination Guarantee:** The Verdict Generator is mechanically restricted from answering using its own pre-trained knowledge base. It can *only* evaluate based on the live Google Search context provided to it.
- **Glass-Box Methodology:** The API returns not just a "True/False", but explicitly returns the exact `fact_checks` and `explanation` it used to reach its conclusion.
- **Stateless & Scalable:** By offloading state to Firebase Firestore and containerizing the Python execution layer in Google Cloud Run, TruthLens can safely scale from 1 user to 10,000 concurrently.

## 💻 Tech Stack
*   **Google Gemini 1.5 Pro / Flash Vision** (Multi-modal inference & Structured Outputs)
*   **Google Custom Search API** (Live Context Retrieval)
*   **FastAPI / Python** (Orchestration Backend)
*   **Vanilla JS / HTML / CSS** (Ultra-fast minimal frontend)
*   **Google Cloud Run & Firebase** (Deployment Network)

## 🛠 How to Run Locally

1. **Clone the Repo & Setup Env:**
   ```bash
   git clone [your_repo_link]
   cd win-prompt/execution
   ```
   Add your `GEMINI_API_KEY`, `GOOGLE_SEARCH_API_KEY`, and `GOOGLE_SEARCH_CX` to the `.env` file.

2. **Start the Orchestration API:**
   ```bash
   pip install -r requirements.txt
   python ../orchestration/api.py
   ```
3. **Launch the UI:**
   Open `win-prompt/frontend/index.html` in your browser.
