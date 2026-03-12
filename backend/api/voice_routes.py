"""Voice API routes — STT and TTS endpoints."""

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import Response

from database.models import TTSRequest, STTResponse
from database.database import log_event
from services.voice_service import speech_to_text, text_to_speech
from utils.logger import log

router = APIRouter()


@router.post("/api/voice/stt", response_model=STTResponse)
async def stt(file: UploadFile = File(...)):
    """
    Speech-to-Text endpoint.
    Accepts an audio file upload and returns transcribed text.
    """
    if file is None or file.filename is None:
        raise HTTPException(status_code=422, detail="Audio file is required")

    log.info("STT request | filename=%s content_type=%s", file.filename, file.content_type)

    try:
        audio_bytes = await file.read()
        if not audio_bytes:
            raise HTTPException(status_code=422, detail="Empty audio file")

        text = await speech_to_text(audio_bytes, filename=file.filename or "audio.webm")

        if not text:
            await log_event("stt_empty | no transcription result")
            return STTResponse(text="")

        await log_event(f"stt_success | text={text[:50]}")
        return STTResponse(text=text)

    except HTTPException:
        raise
    except RuntimeError as exc:
        log.error("STT failed: %s", exc)
        await log_event(f"stt_error | {exc}")
        raise HTTPException(status_code=500, detail=str(exc))
    except Exception as exc:
        log.error("STT unexpected error: %s", exc)
        await log_event(f"stt_error | {exc}")
        raise HTTPException(status_code=500, detail=f"Speech recognition failed: {exc}")


@router.post("/api/voice/tts")
async def tts(req: TTSRequest):
    """
    Text-to-Speech endpoint.
    Accepts text and speed, returns WAV audio.
    """
    log.info("TTS request | text=%s speed=%s", req.text[:60], req.speed)

    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Text is required")

    try:
        audio_bytes = text_to_speech(req.text, speed=req.speed)
        await log_event(f"tts_success | bytes={len(audio_bytes)}")

        return Response(
            content=audio_bytes,
            media_type="audio/wav",
            headers={
                "Content-Disposition": "attachment; filename=jarvis_speech.wav",
            },
        )

    except RuntimeError as exc:
        log.error("TTS failed: %s", exc)
        await log_event(f"tts_error | {exc}")
        raise HTTPException(status_code=500, detail=str(exc))
    except Exception as exc:
        log.error("TTS unexpected error: %s", exc)
        await log_event(f"tts_error | {exc}")
        raise HTTPException(status_code=500, detail=f"Text-to-speech failed: {exc}")
