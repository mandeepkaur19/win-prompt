import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

def extract_text_from_image(file_path: str) -> str:
    """
    Normalizes image inputs into parsable text.
    """
    try:
        # Using Gemini Pro Vision (or 1.5 flash) to describe the image/extract text
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Uploading the file first to the File API
        # Note: In production with FastAPI, we might receive bytes directly. 
        # This implementation assumes the file is temporarily saved to disk.
        sample_file = genai.upload_file(path=file_path)
        
        prompt = "Extract all readable text from this image exactly as written. If there is no explicit text but a clear claim is implied by the image or meme, summarize that core claim concisely. Do not use conversational filler."
        
        response = model.generate_content([sample_file, prompt])
        
        # Cleanup
        genai.delete_file(sample_file.name)
        
        return response.text.strip()
    except Exception as e:
        return f"Error extracting text from image: {str(e)}"

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print(extract_text_from_image(sys.argv[1]))
