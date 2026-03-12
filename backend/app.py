"""Jarvis Core AI — FastAPI backend entry point."""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.settings import BACKEND_HOST, BACKEND_PORT, CORS_ORIGINS, SARVAM_API_KEY
from database.database import init_db
from api.chat_routes import router as chat_router
from api.voice_routes import router as voice_router
from api.system_routes import router as system_router
from utils.logger import log

# ── App ────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Jarvis Core AI Backend",
    description="FastAPI backend for the Jarvis intelligent assistant",
    version="1.0.0",
)

# ── CORS ───────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routes ─────────────────────────────────────────────────────────────
app.include_router(chat_router)
app.include_router(voice_router)
app.include_router(system_router)


# ── Events ─────────────────────────────────────────────────────────────
@app.on_event("startup")
async def startup():
    log.info("=" * 60)
    log.info("  Jarvis Core AI Backend starting...")
    log.info("  Host: %s:%d", BACKEND_HOST, BACKEND_PORT)
    log.info("  CORS origins: %s", CORS_ORIGINS)
    log.info("  Sarvam API key: %s", "configured" if SARVAM_API_KEY else "NOT SET (mock mode)")
    log.info("=" * 60)
    await init_db()


# ── Health ─────────────────────────────────────────────────────────────
@app.get("/api/health")
async def health():
    return {
        "status": "ok",
        "service": "jarvis-core-ai",
        "sarvam_connected": bool(SARVAM_API_KEY),
    }


# ── Run ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host=BACKEND_HOST,
        port=BACKEND_PORT,
        reload=True,
        log_level="info",
    )
