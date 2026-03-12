"""Voice services — Speech-to-Text and Text-to-Speech."""

import io
import tempfile
import threading
import time
import wave
from pathlib import Path

from utils.logger import log


# ── Speech-to-Text ─────────────────────────────────────────────────────

async def speech_to_text(audio_bytes: bytes, filename: str = "audio.webm") -> str:
    """
    Transcribe audio bytes to text using SpeechRecognition library.
    Supports WAV, WEBM, and other common audio formats.
    """
    import speech_recognition as sr

    recognizer = sr.Recognizer()

    # Write audio to a temp file so SpeechRecognition can read it
    suffix = Path(filename).suffix or ".webm"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(audio_bytes)
        tmp_path = tmp.name

    try:
        # If the audio is not WAV, try to handle it directly
        # SpeechRecognition works best with WAV; for webm we use the raw file
        with sr.AudioFile(tmp_path) as source:
            audio_data = recognizer.record(source)

        text = recognizer.recognize_google(audio_data)
        log.info("STT transcribed: %s", text[:100])
        return text

    except sr.UnknownValueError:
        log.warning("STT could not understand audio")
        return ""
    except sr.RequestError as exc:
        log.error("STT service error: %s", exc)
        raise RuntimeError(f"Speech recognition service error: {exc}") from exc
    except Exception as exc:
        log.error("STT error: %s", exc)
        raise RuntimeError(f"Speech-to-text failed: {exc}") from exc
    finally:
        Path(tmp_path).unlink(missing_ok=True)


# ── Text-to-Speech ─────────────────────────────────────────────────────

_tts_lock = threading.Lock()


def text_to_speech(text: str, speed: float = 1.0) -> bytes:
    """
    Convert text to speech using pyttsx3.
    Returns WAV audio bytes.
    Uses a thread lock to prevent concurrent SAPI engine access on Windows.
    """
    try:
        import pyttsx3
    except ImportError:
        raise RuntimeError(
            "Text-to-speech is not available on this server. "
            "pyttsx3 requires a desktop environment (Windows/macOS)."
        )

    # Clamp speed to safe range
    speed = max(0.5, min(2.0, speed))

    # Retry up to 2 times for Windows COM object issues
    last_error = None
    for attempt in range(2):
        engine = None
        tmp_path = None
        try:
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                tmp_path = tmp.name

            with _tts_lock:
                engine = pyttsx3.init()

                # Set speech rate — clamp to safe engine range
                default_rate = engine.getProperty("rate") or 200
                target_rate = max(80, min(350, int(default_rate * speed)))
                engine.setProperty("rate", target_rate)
                engine.setProperty("volume", 1.0)

                engine.save_to_file(text, tmp_path)
                engine.runAndWait()

                # Explicit cleanup before releasing lock
                try:
                    engine.stop()
                except Exception:
                    pass
                engine = None

            # Read outside the lock
            if Path(tmp_path).exists() and Path(tmp_path).stat().st_size > 0:
                with open(tmp_path, "rb") as f:
                    audio_bytes = f.read()
                log.info("TTS generated audio (%d bytes, speed=%.1f) for: %s", len(audio_bytes), speed, text[:60])
                return audio_bytes
            else:
                raise RuntimeError("pyttsx3 produced empty audio file")

        except Exception as exc:
            last_error = exc
            log.warning("TTS attempt %d failed: %s", attempt + 1, exc)
            if engine:
                try:
                    engine.stop()
                except Exception:
                    pass
            time.sleep(0.5)

        finally:
            if tmp_path:
                Path(tmp_path).unlink(missing_ok=True)

    raise RuntimeError(f"Text-to-speech failed after retries: {last_error}")

