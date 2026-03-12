"""Chat API routes — POST /api/chat."""

import time
import uuid

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from database.models import ChatRequest, ChatResponse
from database.database import (
    ensure_conversation,
    save_message,
    get_conversation_messages,
    log_event,
)
from services.sarvam_service import chat_completion
from services.stream_service import stream_chat_response
from services.intent_service import detect_intent
from tools.system_tools import execute_command
from utils.logger import log

router = APIRouter()

# Map frontend model names to actual Sarvam API model
# Sarvam currently only supports 'sarvam-m'
_MODEL_MAP = {
    "sarvam-m": "sarvam-m",
    "sarvam-m-lite": "sarvam-m",
    "sarvam-m-pro": "sarvam-m",
}



@router.post("/api/chat")
async def chat(req: ChatRequest):
    """
    Main chat endpoint.
    - If stream=true  → returns SSE StreamingResponse
    - If stream=false → returns JSON ChatResponse
    """
    log.info(
        "Chat request | convo=%s model=%s stream=%s msg=%s",
        req.conversation_id,
        req.model,
        req.stream,
        req.message[:80],
    )
    await log_event(f"chat_request | convo={req.conversation_id} | model={req.model}")

    try:
        # ── Intent detection ───────────────────────────────────────
        intent_type, command, value = detect_intent(req.message)

        if intent_type == "system_command":
            log.info("System command detected: %s(%s)", command, value)
            result = execute_command(command, value)
            await log_event(f"system_command | {command}={value} | success={result['success']}")

            # Build a descriptive AI response about the command result
            if result["success"]:
                content = f"✅ **Command executed:** `{command}`\n\n{result.get('output', 'Done.')}"
            else:
                content = f"❌ **Command failed:** `{command}`\n\n{result.get('error', 'Unknown error.')}"

            # Save messages to DB
            await ensure_conversation(req.conversation_id)
            user_ts = int(time.time() * 1000)
            await save_message(str(uuid.uuid4()), req.conversation_id, "user", req.message, user_ts)
            ai_msg_id = str(uuid.uuid4())
            ai_ts = int(time.time() * 1000)
            await save_message(ai_msg_id, req.conversation_id, "assistant", content, ai_ts)

            return ChatResponse(id=ai_msg_id, role="assistant", content=content, timestamp=ai_ts)

        # ── Chat with AI ───────────────────────────────────────────
        # Resolve model name to actual Sarvam API model
        resolved_model = _MODEL_MAP.get(req.model, "sarvam-m")
        log.info("Model resolved: %s -> %s", req.model, resolved_model)

        # Fetch conversation history for context
        history = await get_conversation_messages(req.conversation_id, limit=20)

        if req.stream:
            return StreamingResponse(
                stream_chat_response(
                    message=req.message,
                    conversation_id=req.conversation_id,
                    history=history,
                    model=resolved_model,
                    system_prompt=req.system_prompt,
                    temperature=req.temperature,
                    max_tokens=req.max_tokens,
                ),
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "X-Accel-Buffering": "no",
                },
            )

        # ── Non-streaming response ─────────────────────────────────
        await ensure_conversation(req.conversation_id)

        # Save user message
        user_msg_id = str(uuid.uuid4())
        user_ts = int(time.time() * 1000)
        await save_message(user_msg_id, req.conversation_id, "user", req.message, user_ts)

        # Get AI response
        content = await chat_completion(
            req.message,
            history,
            model=resolved_model,
            system_prompt=req.system_prompt,
            temperature=req.temperature,
            max_tokens=req.max_tokens,
        )

        # Save AI message
        ai_msg_id = str(uuid.uuid4())
        ai_ts = int(time.time() * 1000)
        await save_message(ai_msg_id, req.conversation_id, "assistant", content, ai_ts)

        await log_event(f"chat_response | convo={req.conversation_id} | len={len(content)}")
        return ChatResponse(id=ai_msg_id, role="assistant", content=content, timestamp=ai_ts)

    except Exception as exc:
        log.error("Chat endpoint error: %s", exc)
        await log_event(f"chat_error | {exc}")
        raise HTTPException(status_code=500, detail=f"Chat processing failed: {exc}")
