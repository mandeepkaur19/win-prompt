import os
import json
import google.generativeai as genai
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

class VerdictResponse(BaseModel):
    truth_score: int
    verdict: str
    explanation: str
    fact_checks: list[str]
    confidence: str

def generate_truth_score(claim_text: str, retrieved_context: str) -> dict:
    """
    Synthesizes the claim against retrieved context to produce a verdict.
    """
    try:
        # Read the prompt template
        prompt_path = os.path.join(os.path.dirname(__file__), "prompts", "claim_analyzer_prompt.txt")
        if os.path.exists(prompt_path):
            with open(prompt_path, "r", encoding="utf-8") as f:
                system_prompt = f.read()
        else:
            system_prompt = "You are a strict fact checker. Compare the CLAIM against the EVIDENCE and output a clear evaluation."

        prompt = f"""
        {system_prompt}
        
        *** INPUTS ***
        [INPUT_TEXT]: {claim_text}
        
        [EVIDENCE]: 
        {retrieved_context}
        """

        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(
            prompt,
             generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
                response_schema=VerdictResponse,
                temperature=0.1
            )
        )
        
        return json.loads(response.text)
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
