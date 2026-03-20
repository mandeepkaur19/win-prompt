import sys
import os
# Add execution folder to path so we can import the scripts
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'execution'))

from fastapi import FastAPI, HTTPException, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from image_to_text_extractor import extract_text_from_image
from claim_analyzer import analyze_claims
from fact_check_retriever import retrieve_fact_checks
from truth_score_generator import generate_truth_score
from response_formatter import format_and_store_response

app = FastAPI(title="TruthLens API")

# Allow UI to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze_input(text: Optional[str] = Form(None), file: Optional[UploadFile] = None):
    input_text = ""
    
    # Layer 2: Orchestration Pipeline
    
    # 1. Ingest
    if file:
        # Save temp file
        temp_path = f"temp_{file.filename}"
        with open(temp_path, "wb") as f:
            f.write(await file.read())
        try:
            input_text = extract_text_from_image(temp_path)
            if input_text.startswith("Error"):
                raise HTTPException(status_code=500, detail=input_text)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
    elif text:
        input_text = text
    else:
        raise HTTPException(status_code=400, detail="Must provide text or file.")
        
    # 2. Extract Claims
    claims = analyze_claims(input_text)
    if not claims:
        # Fallback if no specific claim found, analyze the whole text
        claims = [{"claim_id": "0", "claim_text": input_text}]
        
    verdicts = []
    
    # 3 & 4. Search and Generate Verdict
    for claim in claims:
        claim_text = claim.get("claim_text", "")
        if not claim_text.strip():
            continue
            
        # Fact check
        context_result = retrieve_fact_checks(claim_text)
        retrieved_context = context_result.get("retrieved_context", "")
        
        # Generate verdict
        verdict = generate_truth_score(claim_text, retrieved_context)
        verdict["claim_text"] = claim_text
        verdicts.append(verdict)
        
    # 5. Format and Store
    final_output = format_and_store_response(verdicts)
    
    return final_output

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8080, reload=True)
