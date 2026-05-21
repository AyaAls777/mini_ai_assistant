
import requests

#detect user intent
def detect_intent(user_message):

    # AI prompt
    prompt = f"""
    You are an intent classifier.

    Available intents:
    - hotel_search
    - flight_search
    - refund_request
    - complaint
    - escalation
    - order_tracking

    Return ONLY one exact intent name.
    Do not explain.
    Do not add extra text.

    User message:
    {user_message}
    """

    #Send POST request to Ollama local API
    response = requests.post(

        "http://localhost:11434/api/generate",

        # Data sent to Ollama
        json={

            #AI model to use
            "model": "llama3",

            #Prompt sent to the AI
            "prompt": prompt,

            "stream": False
        }
    )

    #Convert Ollama response from JSON into Python dictionary
    result = response.json()

    #Return only the AI response text
    #strip() removes extra spaces/new lines
    return result["response"].strip()
