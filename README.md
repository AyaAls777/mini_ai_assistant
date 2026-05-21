# AI Customer Support Assistant

A local AI-powered customer support assistant built with FastAPI, Ollama, and Streamlit.

The system accepts user messages, detects intent using a locally running LLM, routes the request to mock tools, stores short-term memory, and returns structured JSON responses for the frontend to render.

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

## Tech Stack

- Python
- FastAPI
- Ollama
- Streamlit
- Pydantic
- Requests

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

## How It Works

1. The user enters a message in the Streamlit frontend.
2. Streamlit sends the message to the FastAPI `/chat` endpoint.
3. FastAPI sends the message to Ollama for intent detection.
4. Ollama returns an intent such as `hotel_search` or `flight_search`.
5. FastAPI routes the request to the correct tool.
6. The tool returns structured JSON.
7. Streamlit reads the `ui_type` field and displays the correct UI.

---

## Current Memory Logic

The app stores the last few conversation turns in memory.

Each memory item contains:

```json
{
  "user_message": "find flights to london",
  "intent": "flight_search"
}
```

This allows the backend to handle follow-up messages like:

```text
show cheaper ones
```

If the last intent was `flight_search`, the backend returns cheaper flights.

---

## Improvements & Future Enhancements

### Smarter Conversational Memory

Currently, follow-up handling is partially rule-based.

For example, the backend checks conditions like:

```python
if "cheaper" in user_message and last_intent == "flight_search":
```

While this works, it is still somewhat literal and keyword-dependent.

A more advanced approach would be to let the LLM understand the conversation context dynamically instead of manually checking words.

Example future flow:

Conversation history:

```text
User: find flights to london
Intent: flight_search

Current message:
show cheaper ones
```

The AI could then return structured understanding such as:

```json
{
  "intent": "flight_search",
  "modifier": "cheaper"
}
```

This would allow the assistant to naturally understand variations like:

- cheaper options
- low-cost flights
- budget ones
- less expensive hotels
- affordable choices
- anything cheaper?
- show budget hotels instead

without manually hardcoding specific keywords.

---

### Better Structured AI Responses

The LLM can be upgraded to return structured JSON instead of plain text.

Example:

```json
{
  "intent": "hotel_search",
  "location": "Dubai",
  "modifier": "cheaper"
}
```

This would make the backend more scalable and easier to extend.

---

### Improved Frontend

The Streamlit frontend can be enhanced with:

- chat-style interface
- conversation history
- cards with images
- animations/loading states
- dark/light mode
- better UI styling
- sidebar navigation

---

### Additional Tools

The architecture allows easy expansion with new tools such as:

- refund requests
- complaint handling
- escalation support
- order tracking
- ticket management

Each tool can remain modular in its own file.

---

## Offline Operation

After installing dependencies and downloading the Ollama model, the app runs locally without using external AI APIs.
No OpenAI, Claude, or external hotel/flight APIs are used.
