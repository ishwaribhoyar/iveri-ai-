"""Intent detection — classifies user input as chat, system command, or file operation."""

import re
import urllib.parse
from typing import Tuple

# ── Exact-match keywords ────────────────────────────────────────────
_SYSTEM_KEYWORDS: dict[str, str] = {
    "open notepad": "open_app:notepad",
    "open calculator": "open_app:calc",
    "open browser": "open_website:https://www.google.com",
    "open chrome": "open_app:chrome",
    "open google chrome": "open_app:chrome",
    "open firefox": "open_app:firefox",
    "open edge": "open_app:msedge",
    "open cmd": "open_app:cmd",
    "open terminal": "open_app:cmd",
    "open command prompt": "open_app:cmd",
    "open file explorer": "open_app:explorer",
    "open task manager": "open_app:taskmgr",
    "open paint": "open_app:mspaint",
    "open word": "open_app:winword",
    "open excel": "open_app:excel",
    "open powerpoint": "open_app:powerpnt",
    "open spotify": "open_app:spotify",
    "open vscode": "open_app:code",
    "open visual studio code": "open_app:code",
    "open vs code": "open_app:code",
    "close notepad": "close_app:notepad",
    "close chrome": "close_app:chrome",
    "close firefox": "close_app:firefox",
    "take screenshot": "take_screenshot:",
    "take a screenshot": "take_screenshot:",
    "capture screen": "take_screenshot:",
    "screenshot": "take_screenshot:",
    "system info": "system_info:",
    "system information": "system_info:",
    "system status": "system_info:",
    "battery": "system_info:",
    "battery status": "system_info:",
    "cpu usage": "system_info:",
    "memory usage": "system_info:",
    "ram usage": "system_info:",
    "disk usage": "system_info:",
    "open youtube": "open_website:https://www.youtube.com",
    "open google": "open_website:https://www.google.com",
    "open gmail": "open_website:https://mail.google.com",
    "open github": "open_website:https://github.com",
    "open twitter": "open_website:https://twitter.com",
    "open whatsapp": "open_website:https://web.whatsapp.com",
    "open instagram": "open_website:https://www.instagram.com",
    "open facebook": "open_website:https://www.facebook.com",
    "open linkedin": "open_website:https://www.linkedin.com",
    "open reddit": "open_website:https://www.reddit.com",
    "open chatgpt": "open_website:https://chat.openai.com",
    "open stackoverflow": "open_website:https://stackoverflow.com",
}


# ── Regex patterns for natural language ─────────────────────────────
_YOUTUBE_PATTERNS = [
    # "play X on youtube", "open X on youtube", "search X on youtube"
    r"(?:play|open|search|find|watch|put on)\s+(.+?)\s+(?:on|in)\s+youtube",
    # "youtube X", "youtube search X"
    r"youtube\s+(?:search\s+)?(.+)",
    # "search youtube for X"
    r"search\s+youtube\s+(?:for\s+)?(.+)",
    # "play X song", "play X music" (assume YouTube)
    r"play\s+(.+?)\s+(?:song|music|video|clip)",
    # "play X" (general - assume YouTube for media)
    r"^play\s+(.+)$",
]

_GOOGLE_SEARCH_PATTERNS = [
    # "search for X", "google X", "search X on google"
    r"(?:search|look up|find)\s+(?:for\s+)?(.+?)\s+(?:on|in)\s+google",
    r"google\s+(?:search\s+)?(.+)",
    r"search\s+(?:for\s+)?(.+?)\s+(?:on|in)\s+the\s+(?:web|internet)",
    r"search\s+(?:for\s+|on\s+)?(?:google\s+)?(.+)",
]


def detect_intent(message: str) -> Tuple[str, str, str]:
    """
    Detect the intent of a user message.

    Returns:
        (intent_type, command, value)

        intent_type: "chat" | "system_command"
        command: the system command name (empty if chat)
        value: the command argument (empty if chat)
    """
    lower = message.lower().strip()

    # ── 1. Check for direct system command keywords ─────────────────
    for keyword, action in _SYSTEM_KEYWORDS.items():
        if keyword in lower:
            command, _, value = action.partition(":")
            return ("system_command", command, value)

    # ── 2. YouTube patterns ─────────────────────────────────────────
    for pattern in _YOUTUBE_PATTERNS:
        match = re.search(pattern, lower)
        if match:
            query = match.group(1).strip()
            # Remove trailing words like "on youtube" that might have slipped through
            query = re.sub(r"\s+on\s+youtube\s*$", "", query)
            url = f"https://www.youtube.com/results?search_query={urllib.parse.quote_plus(query)}"
            return ("system_command", "open_website", url)

    # ── 3. Google search patterns ───────────────────────────────────
    for pattern in _GOOGLE_SEARCH_PATTERNS:
        match = re.search(pattern, lower)
        if match:
            query = match.group(1).strip()
            # Don't match if it's a very short/generic phrase
            if len(query) > 2:
                url = f"https://www.google.com/search?q={urllib.parse.quote_plus(query)}"
                return ("system_command", "open_website", url)

    # ── 4. Social media profile patterns ────────────────────────────
    social_profile_patterns = [
        # Instagram: "open insta/instagram account/profile of X", "show me X on instagram"
        (r"(?:open|show|go to|visit|find)\s+(?:insta(?:gram)?)\s+(?:account|profile|page|id)?\s*(?:of|for)?\s*(.+)", "https://www.instagram.com/{query}"),
        (r"(?:open|show|go to|visit|find)\s+(.+?)(?:\s+on\s+|\s+in\s+)(?:insta(?:gram)?)", "https://www.instagram.com/{query}"),
        # Twitter/X: "open twitter account of X"
        (r"(?:open|show|go to|visit|find)\s+(?:twitter|x)\s+(?:account|profile|page)?\s*(?:of|for)?\s*(.+)", "https://twitter.com/{query}"),
        (r"(?:open|show|go to|visit|find)\s+(.+?)(?:\s+on\s+|\s+in\s+)(?:twitter|x\.com)", "https://twitter.com/{query}"),
        # Facebook
        (r"(?:open|show|go to|visit|find)\s+(?:facebook|fb)\s+(?:account|profile|page)?\s*(?:of|for)?\s*(.+)", "https://www.facebook.com/{query}"),
        # LinkedIn
        (r"(?:open|show|go to|visit|find)\s+(?:linkedin)\s+(?:account|profile|page)?\s*(?:of|for)?\s*(.+)", "https://www.linkedin.com/in/{query}"),
        # GitHub
        (r"(?:open|show|go to|visit|find)\s+(?:github|gh)\s+(?:account|profile|page|repo)?\s*(?:of|for)?\s*(.+)", "https://github.com/{query}"),
    ]
    for pattern, url_template in social_profile_patterns:
        match = re.search(pattern, lower)
        if match:
            query = match.group(1).strip().replace(" ", "")
            url = url_template.replace("{query}", query)
            return ("system_command", "open_website", url)

    # ── 5. "open ..." pattern ───────────────────────────────────────
    if lower.startswith("open "):
        target = lower[5:].strip()
        if target.startswith("http") or "." in target:
            return ("system_command", "open_website", target)
        # Check if it's a well-known website name
        website_map = {
            "youtube": "https://www.youtube.com",
            "google": "https://www.google.com",
            "gmail": "https://mail.google.com",
            "github": "https://github.com",
            "twitter": "https://twitter.com",
            "facebook": "https://www.facebook.com",
            "instagram": "https://www.instagram.com",
            "insta": "https://www.instagram.com",
            "whatsapp": "https://web.whatsapp.com",
            "linkedin": "https://www.linkedin.com",
            "reddit": "https://www.reddit.com",
            "spotify": "https://open.spotify.com",
        }
        if target in website_map:
            return ("system_command", "open_website", website_map[target])
        # Known desktop apps (short single-word names)
        known_apps = {
            "notepad", "calculator", "calc", "chrome", "firefox", "edge",
            "cmd", "terminal", "explorer", "paint", "word", "excel",
            "powerpoint", "spotify", "vscode", "code", "vlc", "slack",
        }
        if target in known_apps:
            return ("system_command", "open_app", target)
        # If it's a long phrase, it's probably not an app — search Google instead
        if len(target.split()) > 2:
            url = f"https://www.google.com/search?q={urllib.parse.quote_plus(target)}"
            return ("system_command", "open_website", url)
        return ("system_command", "open_app", target)

    # ── 6. "close ..." pattern ──────────────────────────────────────
    if lower.startswith("close "):
        target = lower[6:].strip()
        return ("system_command", "close_app", target)

    # ── 7. Default to chat ──────────────────────────────────────────
    return ("chat", "", "")
