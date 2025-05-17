import requests

from config.config import Config

def call_gemini_api(query, context):
    """ Call Gemini API with query and context """
    try:
        headers = {
            "Content-Type": "application/json"
        }

        # Construct the payload
        payload = {
            "contents": [{
                "parts": [
                    {"text": f"Query: {query}\n\nContext: {context}"}
                ]
            }]
        }

        response = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={Config.GEMINI_API_KEY}",
            json=payload,
            headers=headers
        )

        response.raise_for_status()
        data = response.json()

        # Extract response text
        if "candidates" in data:
            candidate = data["candidates"][0]
            if "content" in candidate and "parts" in candidate["content"]:
                response_text = " ".join([part["text"] for part in candidate["content"]["parts"] if "text" in part])
                return response_text.strip()

        return "No valid response from Gemini API."

    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return "Error in generating response."
