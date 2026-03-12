"""SSE streaming helper — wraps the Sarvam streaming generator into
the `data: {...}\n\n` format the frontend expects."""

import json
import re
import time
import uuid
from typing import AsyncGenerator

from services.sarvam_service import chat_completion_stream
from database.database import ensure_conversation, save_message, log_event
from utils.logger import log


def _strip_think_tags(text: str) -> str:
    """Remove <think>...</think> reasoning blocks.
    If that would leave empty, just remove the tags themselves."""
    cleaned = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    cleaned = re.sub(r"<think>.*$", "", cleaned, flags=re.DOTALL)
    cleaned = cleaned.strip()
    if cleaned:
        return cleaned
    return text.replace("<think>", "").replace("</think>", "").strip()


async def stream_chat_response(
    message: str,
    conversation_id: str,
    history: list[dict],
    *,
    model: str = "sarvam-m",
    system_prompt: str = "",
    temperature: float = 0.7,
    max_tokens: int = 2048,
) -> AsyncGenerator[str, None]:
    """
    Async generator that yields SSE-formatted lines.
    Filters out <think>...</think> reasoning blocks from the AI output.
    If the entire response is in think tags, the content is still shown.
    """
    await ensure_conversation(conversation_id)

    # Save the user message
    user_msg_id = str(uuid.uuid4())
    user_ts = int(time.time() * 1000)
    await save_message(user_msg_id, conversation_id, "user", message, user_ts)

    raw_accumulated = ""
    clean_accumulated = ""
    think_buffer = ""
    in_think = False

    try:
        async for delta in chat_completion_stream(
            message,
            history,
            model=model,
            system_prompt=system_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
        ):
            raw_accumulated += delta

            # Track <think> block boundaries
            if "<think>" in delta:
                in_think = True
                # Remove the opening tag from delta
                delta = delta.replace("<think>", "")
            
            if "</think>" in delta:
                in_think = False
                delta = delta.replace("</think>", "")
                # Skip the closing tag chunk — content already buffered
                if delta.strip():
                    clean_accumulated += delta
                    chunk = json.dumps({"delta": delta, "done": False})
                    yield f"data: {chunk}\n\n"
                continue

            if in_think:
                # Buffer content inside think tags
                think_buffer += delta
            else:
                clean_delta = delta.replace("<think>", "").replace("</think>", "")
                if clean_delta:
                    clean_accumulated += clean_delta
                    chunk = json.dumps({"delta": clean_delta, "done": False})
                    yield f"data: {chunk}\n\n"

    except Exception as exc:
        log.error("Streaming error: %s", exc)
        error_chunk = json.dumps(
            {"delta": f"\n\n⚠️ Error: {exc}", "done": False}
        )
        yield f"data: {error_chunk}\n\n"
        clean_accumulated += f"\n\n⚠️ Error: {exc}"

    # If we only had think-block content (entire response was in think tags),
    # flush the buffered content so the user gets something
    if not clean_accumulated.strip() and think_buffer.strip():
        log.info("Entire response was in <think> tags — flushing buffer")
        flushed = think_buffer.strip()
        clean_accumulated = flushed
        chunk = json.dumps({"delta": flushed, "done": False})
        yield f"data: {chunk}\n\n"

    # Final cleanup
    final_content = clean_accumulated.strip() if clean_accumulated.strip() else _strip_think_tags(raw_accumulated)

    # Save the full AI message (cleaned)
    ai_msg_id = str(uuid.uuid4())
    ai_ts = int(time.time() * 1000)
    await save_message(ai_msg_id, conversation_id, "assistant", final_content, ai_ts)

    # Final done event
    done_payload = json.dumps({
        "delta": "",
        "done": True,
        "id": ai_msg_id,
        "timestamp": ai_ts,
    })
    yield f"data: {done_payload}\n\n"

    await log_event(f"stream_chat | convo={conversation_id} | tokens~{len(final_content.split())}")
    log.info("Stream completed for conversation %s", conversation_id)


