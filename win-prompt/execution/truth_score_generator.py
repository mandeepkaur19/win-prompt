import os
import json
import re
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

def generate_truth_score(claim_text: str, retrieved_context: str) -> dict:
    """
    Synthesizes the claim against retrieved context to produce a verdict.
    """
    try:
        prompt_path = os.path.join(os.path.dirname(__file__), "prompts", "claim_analyzer_prompt.txt")
        if os.path.exists(prompt_path):
            with open(prompt_path, "r", encoding="utf-8") as f:
                system_prompt = f.read()
        else:
            system_prompt = "You are a strict fact checker."

        prompt = f"""
{system_prompt}

*** INPUTS ***
[INPUT_TEXT]: {claim_text}

[EVIDENCE]:
{retrieved_context}

Respond ONLY with a raw JSON object (no markdown, no backticks) with these exact keys:
{{
  "truth_score": <integer 0-100>,
  "verdict": <"True" | "False" | "Misleading" | "Unverifiable">,
  "explanation": <string>,
  "fact_checks": [<string>, ...],
  "confidence": <"Low" | "Medium" | "High">
}}
"""

        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(temperature=0.1)
        )

        raw = response.text.strip()
        # Strip any accidental markdown code fences
        raw = re.sub(r'^```[\w]*\n?', '', raw)
        raw = re.sub(r'\n?```$', '', raw)
        return json.loads(raw.strip())

    except Exception as e:
        return {
            "truth_score": 50,
            "verdict": "Unverifiable",
            "explanation": f"System error generating verdict: {str(e)}",
            "fact_checks": [],
            "confidence": "Low"
        }

if __name__ == "__main__":
    pass
