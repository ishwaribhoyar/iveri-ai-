"""Pydantic models and request/response schemas."""

from pydantic import BaseModel, Field
from typing import Literal, Optional

ALLOWED_MODELS = ["sarvam-m", "sarvam-m-lite", "sarvam-m-pro"]


# ── Database Models ────────────────────────────────────────────────────

class MessageModel(BaseModel):
    id: str
    conversation_id: str
    role: str  # "user" | "assistant"
    content: str
    timestamp: int


class ConversationModel(BaseModel):
    id: str
    created_at: int
    updated_at: int


class LogEntry(BaseModel):
    id: Optional[int] = None
    event: str
    timestamp: int


# ── API Schemas ────────────────────────────────────────────────────────

class ChatRequest(BaseModel):
    message: str
    conversation_id: str
    model: Literal["sarvam-m", "sarvam-m-lite", "sarvam-m-pro"] = "sarvam-m"
    system_prompt: str = "You are Jarvis, an intelligent AI assistant."
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=2048, ge=64, le=8192)
    stream: bool = False


class ChatResponse(BaseModel):
    id: str
    role: str = "assistant"
    content: str
    timestamp: int


class TTSRequest(BaseModel):
    text: str
    speed: float = Field(default=1.0, ge=0.5, le=2.0)


class STTResponse(BaseModel):
    text: str


class SystemCommandRequest(BaseModel):
    command: str
    value: str = ""


class SystemCommandResponse(BaseModel):
    success: bool
    output: str = ""
    error: str = ""
