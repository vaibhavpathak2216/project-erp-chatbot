from __future__ import annotations
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.chatbot_service import chat_with_erp
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import os

app = FastAPI(title="ERP Chatbot", version="1.0.0")

# ── Mount static UI ────────────────────────────────────────────────────────
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# ── Schemas ────────────────────────────────────────────────────────────────
class ChatRequest(BaseModel):
    message: str
    conversation_history: List[Dict[str, Any]] = []

class ChatResponse(BaseModel):
    answer: str
    function_called: Optional[str] = None
    raw_data_fetched: bool = False

# ── Routes ─────────────────────────────────────────────────────────────────
@app.get("/")
async def serve_ui():
    ui_path = os.path.join(static_dir, "index.html")
    if os.path.exists(ui_path):
        return FileResponse(ui_path)
    return {"message": "ERP Chatbot API", "docs": "/docs"}

@app.get("/health")
async def health():
    return {"status": "ok", "service": "ERP Chatbot"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    result = chat_with_erp(
        user_message=request.message,
        conversation_history=request.conversation_history
    )
    return ChatResponse(**result)