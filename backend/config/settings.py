"""Application settings loaded from environment variables."""

import os
from pathlib import Path

# Load .env file if present
_env_path = Path(__file__).resolve().parent.parent / ".env"
if _env_path.exists():
    with open(_env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, value = line.partition("=")
                os.environ.setdefault(key.strip(), value.strip())

# ── Paths ──────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "data" / "jarvis.db"
LOG_DIR = BASE_DIR / "logs"

# ── Sarvam AI ──────────────────────────────────────────────────────────
SARVAM_API_KEY: str = os.getenv("SARVAM_API_KEY", "")
SARVAM_API_URL: str = "https://api.sarvam.ai/v1/chat/completions"
DEFAULT_MODEL: str = "sarvam-m"
DEFAULT_TEMPERATURE: float = 0.7
DEFAULT_MAX_TOKENS: int = 2048
DEFAULT_SYSTEM_PROMPT: str = (
    "You are Jarvis, an intelligent AI assistant. You are helpful, concise, "
    "and knowledgeable. You can assist with general questions, coding, "
    "writing, analysis, and system automation when connected to a backend."
)

# ── Server ─────────────────────────────────────────────────────────────
BACKEND_HOST: str = os.getenv("BACKEND_HOST", "0.0.0.0")
BACKEND_PORT: int = int(os.getenv("PORT", os.getenv("BACKEND_PORT", "8000")))

# ── CORS ───────────────────────────────────────────────────────────────
# Always allow localhost for development
CORS_ORIGINS: list[str] = [
    "http://localhost:8080",
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:8080",
]

# Add production frontend URL from env var
_frontend_url = os.getenv("FRONTEND_URL", "")
if _frontend_url:
    CORS_ORIGINS.append(_frontend_url)
    # Also add without trailing slash
    if _frontend_url.endswith("/"):
        CORS_ORIGINS.append(_frontend_url.rstrip("/"))
    else:
        CORS_ORIGINS.append(_frontend_url + "/")

# If deployed (PORT is set by Render), allow all origins as fallback
if os.getenv("RENDER") or os.getenv("PORT"):
    CORS_ORIGINS.append("*")

# ── Voice ──────────────────────────────────────────────────────────────
TTS_ENGINE: str = os.getenv("TTS_ENGINE", "pyttsx3")   # pyttsx3
STT_ENGINE: str = os.getenv("STT_ENGINE", "google")     # google (via SpeechRecognition)

# ── Safety ─────────────────────────────────────────────────────────────
ALLOWED_SYSTEM_COMMANDS: list[str] = [
    "open_app",
    "close_app",
    "open_website",
    "take_screenshot",
    "system_info",
]
