import os
import requests
from dotenv import load_dotenv

load_dotenv()

def retrieve_fact_checks(claim_text: str) -> dict:
    """
    Gathers real-world context for a specific claim using Google Custom Search API.
    Returns: {"claim_text": "...", "retrieved_context": "..."}
    """
    api_key = os.environ.get("GOOGLE_SEARCH_API_KEY")
    cx = os.environ.get("GOOGLE_SEARCH_CX")
    
    if not api_key or not cx:
        return {
            "claim_text": claim_text,
            "retrieved_context": "Error: Google Search API keys not configured. Cannot verify."
        }
        
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": api_key,
        "cx": cx,
        "q": claim_text,
        "num": 3  # Get top 3 snippets for speed
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        snippets = []
        if "items" in data:
            for item in data["items"]:
                snippet = item.get("snippet", "")
                title = item.get("title", "")
                link = item.get("link", "")
                snippets.append(f"Source: {title} ({link})\nContext: {snippet}")
                
        retrieved_context = "\n\n".join(snippets) if snippets else "No relevant search results found."
        
        return {
            "claim_text": claim_text,
            "retrieved_context": retrieved_context
        }
    except Exception as e:
        return {
            "claim_text": claim_text,
            "retrieved_context": f"Error retrieving context: {str(e)}"
        }

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print(retrieve_fact_checks(sys.argv[1]))
