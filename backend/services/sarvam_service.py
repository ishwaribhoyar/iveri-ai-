"""Sarvam AI chat completion service.

Calls https://api.sarvam.ai/v1/chat/completions with the official API format.
Falls back to a mock response generator when no API key is configured.
"""

import json
import re
import time
import uuid
from typing import AsyncGenerator

import httpx

from config.settings import SARVAM_API_KEY, SARVAM_API_URL
from utils.logger import log

# Sarvam API currently only supports 'sarvam-m'
# Map frontend model names to the actual API model
_MODEL_MAP = {
    "sarvam-m": "sarvam-m",
    "sarvam-m-lite": "sarvam-m",
    "sarvam-m-pro": "sarvam-m",
}

def _resolve_model(model: str) -> str:
    return _MODEL_MAP.get(model, "sarvam-m")


def _strip_think_tags(text: str) -> str:
    """Remove <think>...</think> reasoning blocks from Sarvam AI output.
    
    If stripping think blocks would leave an empty response,
    falls back to just removing the tags but keeping the content.
    """
    # First try: remove entire think blocks
    cleaned = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    # Also handle unclosed <think> tags
    cleaned = re.sub(r"<think>.*$", "", cleaned, flags=re.DOTALL)
    cleaned = cleaned.strip()
    
    if cleaned:
        return cleaned
    
    # Fallback: if stripping left nothing, just remove the tags but keep content
    fallback = text.replace("<think>", "").replace("</think>", "").strip()
    return fallback


def _build_messages(
    system_prompt: str,
    history: list[dict],
    user_message: str,
) -> list[dict]:
    """Assemble the messages array for the Sarvam API."""
    messages: list[dict] = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    for msg in history:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": user_message})
    return messages


async def chat_completion(
    message: str,
    history: list[dict],
    *,
    model: str = "sarvam-m",
    system_prompt: str = "",
    temperature: float = 0.7,
    max_tokens: int = 2048,
) -> str:
    """Non-streaming chat completion. Returns the full response text."""
    if not SARVAM_API_KEY:
        log.warning("SARVAM_API_KEY not set — using mock response")
        return _mock_response(message)

    messages = _build_messages(system_prompt, history, message)
    resolved = _resolve_model(model)
    log.info("Model resolved: %s -> %s", model, resolved)
    payload = {
        "model": resolved,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": False,
    }
    headers = {
        "Content-Type": "application/json",
        "api-subscription-key": SARVAM_API_KEY,
    }

    async with httpx.AsyncClient(timeout=90.0) as client:
        resp = await client.post(SARVAM_API_URL, json=payload, headers=headers)
        resp.raise_for_status()
        data = resp.json()

    content = data["choices"][0]["message"]["content"]
    content = _strip_think_tags(content)
    log.info("Sarvam response received (%d chars)", len(content))
    return content


async def chat_completion_stream(
    message: str,
    history: list[dict],
    *,
    model: str = "sarvam-m",
    system_prompt: str = "",
    temperature: float = 0.7,
    max_tokens: int = 2048,
) -> AsyncGenerator[str, None]:
    """Streaming chat completion. Yields content delta strings."""
    if not SARVAM_API_KEY:
        log.warning("SARVAM_API_KEY not set — using mock streaming response")
        async for chunk in _mock_stream(message):
            yield chunk
        return

    messages = _build_messages(system_prompt, history, message)
    payload = {
        "model": _resolve_model(model),
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": True,
    }
    headers = {
        "Content-Type": "application/json",
        "api-subscription-key": SARVAM_API_KEY,
    }

    async with httpx.AsyncClient(timeout=180.0) as client:
        async with client.stream(
            "POST", SARVAM_API_URL, json=payload, headers=headers
        ) as resp:
            resp.raise_for_status()
            async for line in resp.aiter_lines():
                if not line.startswith("data:"):
                    continue
                raw = line[len("data:"):].strip()
                if raw == "[DONE]":
                    break
                try:
                    chunk = json.loads(raw)
                    delta = chunk.get("choices", [{}])[0].get("delta", {})
                    content = delta.get("content", "")
                    if content:
                        yield content
                except (json.JSONDecodeError, IndexError, KeyError):
                    continue


# ── Fallback mock responses (when no API key) ─────────────────────────

import asyncio
import random

_MOCK_RESPONSES = [
    "Hello! I'm **Jarvis**, your AI assistant. I'm currently running in **mock mode** because no Sarvam API key is configured.\n\nTo enable real AI responses, set the `SARVAM_API_KEY` environment variable and restart the backend.\n\nI can still demonstrate the full chat interface — try asking me anything!",
    "That's a great question! In mock mode, I generate placeholder responses to test the system.\n\nHere's what you need to do to get real AI:\n\n1. Sign up at [Sarvam AI](https://dashboard.sarvam.ai/)\n2. Get your API subscription key\n3. Set `SARVAM_API_KEY=your_key` in your environment\n4. Restart the backend\n\nThe streaming and all other features will work the same way!",
    "I've processed your message. Here's a demo response:\n\n```python\n# This is a mock response\ndef get_ai_response(message: str) -> str:\n    return \"Connect to Sarvam AI for real responses!\"\n```\n\nThe system is working correctly — just needs an API key for real AI inference.",
    "Analyzing your input...\n\n| Feature | Status |\n|---------|--------|\n| Chat API | ✅ Working |\n| Streaming | ✅ Working |\n| Voice STT | ✅ Working |\n| Voice TTS | ✅ Working |\n| AI Model | ⚠️ Mock Mode |\n\nSet `SARVAM_API_KEY` to connect to Sarvam AI!",
]


def _mock_response(message: str) -> str:
    """Simple mock response for testing without an API key."""
    lower = message.lower()
    if any(w in lower for w in ("hello", "hi", "hey")):
        return _MOCK_RESPONSES[0]
    if any(w in lower for w in ("help", "what can you do")):
        return _MOCK_RESPONSES[3]
    return random.choice(_MOCK_RESPONSES)


async def _mock_stream(message: str) -> AsyncGenerator[str, None]:
    """Simulate a streaming response for testing."""
    full_text = _mock_response(message)
    words = full_text.split(" ")
    for i, word in enumerate(words):
        token = word if i == 0 else " " + word
        yield token
        await asyncio.sleep(0.01 + random.random() * 0.02)
