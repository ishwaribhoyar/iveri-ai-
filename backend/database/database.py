"""SQLite database layer — async via aiosqlite."""

import aiosqlite
import time
from pathlib import Path

from config.settings import DATABASE_PATH
from utils.logger import log

_db_path: Path = DATABASE_PATH


async def init_db() -> None:
    """Create tables if they don't exist."""
    _db_path.parent.mkdir(parents=True, exist_ok=True)
    async with aiosqlite.connect(_db_path) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id TEXT PRIMARY KEY,
                created_at INTEGER NOT NULL,
                updated_at INTEGER NOT NULL
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id TEXT PRIMARY KEY,
                conversation_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp INTEGER NOT NULL,
                FOREIGN KEY (conversation_id) REFERENCES conversations(id)
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event TEXT NOT NULL,
                timestamp INTEGER NOT NULL
            )
        """)
        await db.execute(
            "CREATE INDEX IF NOT EXISTS idx_messages_convo ON messages(conversation_id)"
        )
        await db.commit()
    log.info("Database initialised at %s", _db_path)


async def ensure_conversation(conversation_id: str) -> None:
    """Create conversation record if it doesn't exist."""
    now = int(time.time() * 1000)
    async with aiosqlite.connect(_db_path) as db:
        row = await db.execute(
            "SELECT id FROM conversations WHERE id = ?", (conversation_id,)
        )
        if await row.fetchone() is None:
            await db.execute(
                "INSERT INTO conversations (id, created_at, updated_at) VALUES (?, ?, ?)",
                (conversation_id, now, now),
            )
            await db.commit()


async def save_message(
    message_id: str,
    conversation_id: str,
    role: str,
    content: str,
    timestamp: int,
) -> None:
    """Insert a message and update the conversation's updated_at."""
    async with aiosqlite.connect(_db_path) as db:
        await db.execute(
            "INSERT OR REPLACE INTO messages (id, conversation_id, role, content, timestamp) "
            "VALUES (?, ?, ?, ?, ?)",
            (message_id, conversation_id, role, content, timestamp),
        )
        await db.execute(
            "UPDATE conversations SET updated_at = ? WHERE id = ?",
            (timestamp, conversation_id),
        )
        await db.commit()


async def get_conversation_messages(
    conversation_id: str, limit: int = 50
) -> list[dict]:
    """Return recent messages for a conversation, oldest-first."""
    async with aiosqlite.connect(_db_path) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT id, role, content, timestamp FROM messages "
            "WHERE conversation_id = ? ORDER BY timestamp DESC LIMIT ?",
            (conversation_id, limit),
        )
        rows = await cursor.fetchall()
    # Return oldest-first so they can be appended to the prompt in order
    return [dict(r) for r in reversed(rows)]


async def log_event(event: str) -> None:
    """Write an event to the logs table."""
    now = int(time.time() * 1000)
    try:
        async with aiosqlite.connect(_db_path) as db:
            await db.execute(
                "INSERT INTO logs (event, timestamp) VALUES (?, ?)",
                (event, now),
            )
            await db.commit()
    except Exception as exc:
        log.error("Failed to log event: %s", exc)
