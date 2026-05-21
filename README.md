# AI Customer Support Assistant

A local AI-powered customer support assistant built with FastAPI, Ollama, and Streamlit.

The system accepts user messages, detects intent using a locally running LLM, routes the request to mock tools, stores short-term memory, and returns structured JSON responses for the frontend to render.

---

## Prerequisites

Before running the project, make sure you have:

- Python 3 installed
- Ollama installed
- Llama3 model downloaded through Ollama
- Required Python packages installed:
  - fastapi
  - uvicorn
  - requests
  - streamlit
  - pydantic

---

## Tech Stack

- Python
- FastAPI
- Ollama
- Streamlit
- Pydantic
- Requests

---

## Features

- Local AI intent detection using Ollama
- FastAPI backend with `/chat` endpoint
- Streamlit frontend
- Mock hotel and flight tools
- Structured JSON responses
- Short-term memory for follow-up questions
- Dynamic frontend rendering based on `ui_type`
- Fully local/offline after setup

---

## Project Structure

```text
interview_task/
├── backend/
│   ├── main.py
│   ├── services/
│   │   └── ollama_service.py
│   └── tools/
│       ├── hotel_tool.py
│       └── flight_tool.py
│
└── frontend/
    └── streamlit_app.py
```

---

## Architecture Overview

```text
User
 ↓
Streamlit Frontend
 ↓
FastAPI Backend
 ↓
Ollama Local LLM
 ↓
Intent Detection
 ↓
Tool Router
 ↓
Mock Tool Execution
 ↓
Structured JSON Response
 ↓
Streamlit Dynamic UI Rendering
```

---

## Design Decisions

### Local LLM

Ollama is used so the AI model runs locally on the machine. This keeps the project offline after the model has been downloaded.

### FastAPI Backend

FastAPI is used to expose a clean `/chat` API endpoint. The backend handles request validation, intent routing, tool execution, and memory management.

### Streamlit Frontend

Streamlit is used as a simple local frontend to demonstrate the assistant quickly. It sends messages to FastAPI and displays the returned data based on the `ui_type` field.

## Screenshots

All project screenshots can be found in the `/screenshots` folder.

### Tool-Based Architecture

Each task is handled by a separate tool function. For example:

- `hotel_tool()` handles hotel responses
- `flight_tool()` handles flight responses
- `get_cheaper_hotels()` filters cheaper hotel results
- `get_cheaper_flights()` filters cheaper flight results

This keeps the project modular and easier to expand.

### Short-Term Memory

The backend stores the last few conversation turns in memory. This allows the assistant to understand follow-up messages such as:

```text
show cheaper ones
```

after the user previously searched for hotels or flights.

---

## Setup Steps

### 1. Install Python packages

```bash
pip3 install fastapi uvicorn requests streamlit pydantic
```

### 2. Run Ollama model

Make sure Ollama is installed and running.

```bash
ollama run llama3
```

### 3. Run FastAPI backend

From the `backend` folder:

```bash
python3 -m uvicorn main:app --reload
```

The backend will run at:

```text
http://127.0.0.1:8000
```

Swagger API docs are available at:

```text
http://127.0.0.1:8000/docs
```

### 4. Run Streamlit frontend

From the main project folder:

```bash
python3 -m streamlit run frontend/streamlit_app.py
```

The frontend will run at:

```text
http://localhost:8501
```

---

## API Payload Examples

### Hotel Search

Request:

```json
{
  "message": "show hotels in dubai"
}
```

Response:

```json
{
  "message": "Hotels found",
  "ui_type": "hotel_page",
  "data": {
    "hotels": [
      {
        "name": "Grand Palace",
        "price": "$220",
        "rating": 4.8
      },
      {
        "name": "Budget Inn",
        "price": "$90",
        "rating": 4.1
      }
    ]
  }
}
```

---

### Flight Search

Request:

```json
{
  "message": "find flights to london"
}
```

Response:

```json
{
  "message": "Flights found",
  "ui_type": "flight_page",
  "data": {
    "flights": [
      {
        "airline": "Emirates",
        "price": "$450",
        "destination": "London"
      },
      {
        "airline": "Qatar Airways",
        "price": "$850",
        "destination": "London"
      }
    ]
  }
}
```

---

### Follow-Up Question

Request:

```json
{
  "message": "show cheaper ones"
}
```

If the previous intent was `flight_search`, the backend returns:

```json
{
  "message": "Cheaper flights found",
  "ui_type": "flight_page",
  "data": {
    "flights": [
      {
        "airline": "Emirates",
        "price": "$450",
        "destination": "London"
      }
    ]
  }
}
```

---

## curl Instructions

### Hotel Search

```bash
curl -X POST "http://127.0.0.1:8000/chat" \
-H "Content-Type: application/json" \
-d '{"message": "show hotels in dubai"}'
```

### Flight Search

```bash
curl -X POST "http://127.0.0.1:8000/chat" \
-H "Content-Type: application/json" \
-d '{"message": "find flights to london"}'
```

### Follow-Up Search

```bash
curl -X POST "http://127.0.0.1:8000/chat" \
-H "Content-Type: application/json" \
-d '{"message": "show cheaper ones"}'
```

---

## Swagger API Testing

FastAPI automatically provides interactive API documentation through Swagger UI.

After starting the backend server, open:

```text
http://127.0.0.1:8000/docs
```

Swagger allows testing API endpoints directly from the browser without needing Postman.

### Example Request

```json
{
  "message": "show hotels in dubai"
}
```

### Steps

1. Open Swagger docs.
2. Expand the `/chat` endpoint.
3. Click `Try it out`.
4. Enter a JSON request body.
5. Click `Execute`.
6. View the JSON response returned by the backend.

---

## Current Memory Logic

The app stores the last few conversation turns in a simple in-memory list.

Each memory item contains:

```json
{
  "user_message": "find flights to london",
  "intent": "flight_search"
}
```

This allows the backend to understand follow-up messages.

Example:

```text
User: find flights to london
Assistant: returns flight results

User: show cheaper ones
Assistant: understands that "ones" refers to flights
```

---

## Offline Operation

After the Python dependencies are installed and the Ollama model is downloaded, the system runs locally.

No OpenAI, Claude, or external hotel/flight APIs are used.

The only local services required are:

- Ollama running locally
- FastAPI running locally
- Streamlit running locally

---

## Improvements & Future Enhancements

### Smarter Conversational Memory

Currently, follow-up handling is partially rule-based.

For example, the backend checks conditions like:

```python
if "cheaper" in user_message and last_intent == "flight_search":
```

While this works, it is still somewhat literal and keyword-dependent.

A better method would be to let the LLM analyze the conversation memory and current message together.

Example future prompt:

```text
Conversation history:
User: find flights to london
Intent: flight_search

Current message:
show cheaper ones

Return JSON:
{
  "intent": "flight_search",
  "modifier": "cheaper"
}
```

This would allow the assistant to understand more natural phrases such as:

- cheaper options
- low-cost flights
- budget ones
- less expensive hotels
- affordable choices
- anything cheaper?
- show budget hotels instead

without manually hardcoding exact keywords.

---

### Structured LLM Output

The LLM can be upgraded to return strict JSON instead of plain text.

Example:

```json
{
  "intent": "hotel_search",
  "location": "Dubai",
  "modifier": "cheaper"
}
```

This would make tool routing more reliable and easier to extend.

---

### Enhanced Memory System

Current memory stores only:

- user message
- detected intent

Future versions could also store:

- extracted entities
- filters
- destinations
- modifiers
- previous results

This would allow more advanced follow-up conversations such as:

```text
find flights to london
only emirates
show cheaper ones
sort by lowest price
```

---

### Additional Tools

The architecture can be expanded with more tools such as:

- refund requests
- complaint handling
- escalation support
- order tracking
- ticket management

Each tool can remain modular in its own file.

---

### Improved Frontend

The Streamlit frontend can be enhanced with:

- chat history display
- cards with images
- sidebar prompt examples
- loading indicators
- improved styling
- responsive layout

---

## Notes

This project uses Streamlit instead of Flutter for the frontend to keep the prototype lightweight and easy to run locally.

The backend architecture still demonstrates the main required AI workflow:

- local LLM intent detection
- tool routing
- structured JSON responses
- short-term memory
- offline operation

## Offline Operation

After installing dependencies and downloading the Ollama model, the app runs locally without using external AI APIs.
No OpenAI, Claude, or external hotel/flight APIs are used.
