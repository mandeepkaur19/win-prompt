import os
import json
import re
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

def analyze_claims(input_text: str) -> list[dict]:
    """
    Identifies specific, verifiable factual claims from messy inputs.
    Returns a list of dicts: {"claim_id": "...", "claim_text": "..."}
    """
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        prompt = f"""
Extract the core, verifiable factual claims from the following text.
Ignore opinions, greetings, or conversational noise.
If there are no verifiable claims, return an empty list.

TEXT TO ANALYZE:
{input_text}

Respond ONLY with a raw JSON object (no markdown, no backticks) in this exact format:
{{"claims": [{{"claim_id": "1", "claim_text": "<claim here>"}}]}}
"""
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(temperature=0.1)
        )

        raw = response.text.strip()
        raw = re.sub(r'^```[\w]*\n?', '', raw)
        raw = re.sub(r'\n?```$', '', raw)
        data = json.loads(raw.strip())
        return data.get("claims", [])
    except Exception as e:
        print(f"Error extracting claims: {e}")
        return []

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print(json.dumps(analyze_claims(sys.argv[1]), indent=2))
