#Testing backend setup with FastAPI
# # Importing FastAPI framework
# from fastapi import FastAPI

# # Creating the FastAPI app
# app = FastAPI()

# # Creating a route for the homepage
# # When someone visits "/" it runs this function
# @app.get("/")
# def home():

#     # Return JSON response
#     return {
#         "message": "Backend working" 
#     }

#---------------------------------------------------
from tools.hotel_tool import hotel_tool
from services.ollama_service import detect_intent
from tools.flight_tool import flight_tool, get_cheaper_flights
from tools.hotel_tool import hotel_tool, get_cheaper_hotels


from fastapi import FastAPI
from pydantic import BaseModel

#Store conversation memory
conversation_memory = []

app = FastAPI()

#Function to save conversation memory
def save_memory(user_message, intent):

    # Add new conversation turn
    conversation_memory.append({
        "user_message": user_message,
        "intent": intent
    })

    if len(conversation_memory) > 5:

        conversation_memory.pop(0) #pop(0) removes the first item in the list, which is the oldest conversation turn, to keep the memory size manageable
        
        print(conversation_memory) #prints to the console for debugging purpose 

def get_last_intent():

    if len(conversation_memory) == 0:
        return None

    # Return the intent from the most recent message
    return conversation_memory[-1]["intent"]      


# Create the request schema
class ChatRequest(BaseModel): #ChatRequest is the name of the schema, it inherits from BaseModel which is a Pydantic class that allows us to define the structure of the data we expect in the request body

    # User message
    message: str

@app.post("/chat")
def chat(request: ChatRequest): #request is the data sent from frontend, it should match the ChatRequest schema

    # Get user message case sensitive
    user_message = request.message.lower()

    last_intent = get_last_intent()
    print(last_intent)

    #Send message to Ollama AI
    #AI returns the detected intent
    intent = detect_intent(user_message) #calling detec intent function from ollama service
    print("LAST INTENT:", last_intent)
    print("CURRENT INTENT:", intent) 
 #-------------------------------------------------------------------------------
    if "cheaper" in user_message and last_intent == "hotel_search":

         save_memory(user_message, "hotel_search")
         return get_cheaper_hotels()

    elif "cheaper" in user_message and last_intent == "flight_search":

            save_memory(user_message, "flight_search")
            return get_cheaper_flights()
    
    save_memory(user_message, intent)

#_--------------------------------------------------------------------------
    # If AI detects hotel search intent
    if intent == "hotel_search":

        return hotel_tool()
    
    if intent == "flight_search":

        return flight_tool()

    # Default response
    return {
        "message": f"You said: {user_message}",
        "ui_type": "text",
        "data": {}
    }
