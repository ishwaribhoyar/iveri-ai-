"""System automation tools — app control, screenshots, system info."""

import os
import platform
import subprocess
import webbrowser
import tempfile
from pathlib import Path

import psutil

from utils.logger import log


def open_app(name: str) -> dict:
    """Launch an application by name."""
    try:
        if platform.system() == "Windows":
            os.startfile(name)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", "-a", name])
        else:
            subprocess.Popen([name])
        log.info("Opened app: %s", name)
        return {"success": True, "output": f"Opened {name}"}
    except Exception as exc:
        log.error("Failed to open app %s: %s", name, exc)
        return {"success": False, "error": str(exc)}


def close_app(name: str) -> dict:
    """Terminate a running process by name."""
    killed = 0
    for proc in psutil.process_iter(["name"]):
        try:
            if name.lower() in (proc.info["name"] or "").lower():
                proc.terminate()
                killed += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    if killed:
        log.info("Closed %d process(es) matching '%s'", killed, name)
        return {"success": True, "output": f"Closed {killed} process(es) matching '{name}'"}
    return {"success": False, "error": f"No running process found matching '{name}'"}


def open_website(url: str) -> dict:
    """Open a URL in the default browser."""
    try:
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        webbrowser.open(url)
        log.info("Opened website: %s", url)
        return {"success": True, "output": f"Opened {url}"}
    except Exception as exc:
        log.error("Failed to open website %s: %s", url, exc)
        return {"success": False, "error": str(exc)}


def take_screenshot() -> dict:
    """Take a screenshot and save to a temp file."""
    try:
        import pyautogui
        screenshot = pyautogui.screenshot()
        tmp_path = Path(tempfile.gettempdir()) / "jarvis_screenshot.png"
        screenshot.save(str(tmp_path))
        log.info("Screenshot saved to %s", tmp_path)
        return {"success": True, "output": f"Screenshot saved to {tmp_path}"}
    except ImportError:
        return {"success": False, "error": "pyautogui not installed — run: pip install pyautogui"}
    except Exception as exc:
        log.error("Screenshot failed: %s", exc)
        return {"success": False, "error": str(exc)}


def system_info() -> dict:
    """Gather system information."""
    try:
        cpu_percent = psutil.cpu_percent(interval=0.5)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage("/") if platform.system() != "Windows" else psutil.disk_usage("C:\\")
        battery = psutil.sensors_battery()

        info_lines = [
            f"**System:** {platform.system()} {platform.release()}",
            f"**Machine:** {platform.machine()}",
            f"**Processor:** {platform.processor() or 'Unknown'}",
            f"**CPU Usage:** {cpu_percent}%",
            f"**RAM:** {mem.percent}% used ({_fmt_bytes(mem.used)} / {_fmt_bytes(mem.total)})",
            f"**Disk:** {disk.percent}% used ({_fmt_bytes(disk.used)} / {_fmt_bytes(disk.total)})",
        ]
        if battery:
            info_lines.append(
                f"**Battery:** {battery.percent}% {'(charging)' if battery.power_plugged else '(on battery)'}"
            )

        output = "\n".join(info_lines)
        log.info("System info gathered")
        return {"success": True, "output": output}
    except Exception as exc:
        log.error("System info failed: %s", exc)
        return {"success": False, "error": str(exc)}


def execute_command(command: str, value: str = "") -> dict:
    """Route a command to the appropriate tool function."""
    handlers = {
        "open_app": lambda: open_app(value),
        "close_app": lambda: close_app(value),
        "open_website": lambda: open_website(value),
        "take_screenshot": lambda: take_screenshot(),
        "system_info": lambda: system_info(),
    }
    handler = handlers.get(command)
    if handler is None:
        return {"success": False, "error": f"Unknown command: {command}"}
    return handler()


def _fmt_bytes(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} PB"
