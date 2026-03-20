import json
import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Firebase on module load
try:
    cred_path = os.environ.get("FIREBASE_CREDENTIALS_PATH", "./firebase_admin.json")
    if os.path.exists(cred_path):
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
    else:
        db = None
        print(f"Warning: Firebase credentials not found at {cred_path}")
except Exception as e:
    db = None
    print(f"Error initializing Firebase: {e}")

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
    
    # Store to Firebase if configured
    if db:
        try:
            doc_ref = db.collection("truthlens_analyses").document()
            doc_ref.set(final_payload)
            final_payload["data"]["firebase_id"] = doc_ref.id
        except Exception as e:
            print(f"Failed to save to Firebase: {e}")
            final_payload["status"] = "partial_success (db_error)"
            
    return final_payload
