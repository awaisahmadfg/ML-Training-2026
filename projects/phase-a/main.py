# projects/phase-a/main.py — minimal skeleton
import asyncio
from fastapi import FastAPI

app = FastAPI(title="Phase A — Async Lab")

@app.get("/health")
async def health():
    return {"ok": True}

# TODO: /ask, broken-block, fixed-block, llm-timeout