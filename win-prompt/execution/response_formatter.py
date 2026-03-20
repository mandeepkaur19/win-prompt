import json
import os
from dotenv import load_dotenv

load_dotenv()

def format_and_store_response(verdicts: list[dict]) -> dict:
    """
    Structures the final output and handles data persistence.
    """
    final_payload = {
        "status": "success",
        "data": {
            "claims_analyzed": len(verdicts),
            "results": verdicts
        }
    }
    return final_payload
