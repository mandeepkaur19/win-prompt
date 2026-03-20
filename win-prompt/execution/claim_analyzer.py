import os
import json
import google.generativeai as genai
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# Define output schema using Pydantic
class Claim(BaseModel):
    claim_id: str
    claim_text: str

class ClaimList(BaseModel):
    claims: list[Claim]

def analyze_claims(input_text: str) -> list[dict]:
    """
    Identifies specific, verifiable factual claims from messy inputs.
    Returns a list of dicts: {"claim_id": "...", "claim_text": "..."}
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
        Extract the core, verifiable factual claims from the following text.
        Ignore opinions, greetings, or conversational noise.
        If there are no verifiable claims, return an empty list.

        TEXT TO ANALYZE:
        {input_text}
        """
        
        response = model.generate_content(
            prompt,
             generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
                response_schema=ClaimList,
                temperature=0.1
            )
        )
        
        data = json.loads(response.text)
        return data.get("claims", [])
    except Exception as e:
        print(f"Error extracting claims: {e}")
        return []

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print(json.dumps(analyze_claims(sys.argv[1]), indent=2))
