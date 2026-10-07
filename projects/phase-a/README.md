# Phase A — FastAPI Async Lab

## Setup
cd projects/phase-a
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload

## Docs
http://127.0.0.1:8000/docs

## Endpoints (lab)
- POST /ask?mode=serial|gather
- GET /broken-block
- GET /fixed-block
- GET /llm-timeout

## Notes
See notes/lab-observations.md