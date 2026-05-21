# AI Customer Support Assistant

A local AI-powered customer support assistant built with FastAPI, Ollama, and Streamlit.

The system accepts user messages, detects intent using a locally running LLM, routes the request to mock tools, stores short-term memory, and returns structured JSON responses for the frontend to render.

## Features

- Local AI intent detection using Ollama
- FastAPI backend with `/chat` endpoint
- Streamlit frontend
- Mock hotel and flight tools
- Structured JSON responses
- Short-term memory for follow-up questions
- Dynamic frontend rendering based on `ui_type`
- Fully local/offline after setup

## Tech Stack

- Python
- FastAPI
- Ollama
- Streamlit
- Pydantic
- Requests

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
