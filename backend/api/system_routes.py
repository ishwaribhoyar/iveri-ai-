"""System automation API routes."""

from fastapi import APIRouter, HTTPException

from database.models import SystemCommandRequest, SystemCommandResponse
from database.database import log_event
from config.settings import ALLOWED_SYSTEM_COMMANDS
from tools.system_tools import execute_command
from utils.logger import log

router = APIRouter()


@router.post("/api/system/execute", response_model=SystemCommandResponse)
async def system_execute(req: SystemCommandRequest):
    """
    Execute a system command.
    Only commands in the ALLOWED_SYSTEM_COMMANDS list are permitted.
    """
    log.info("System execute request | command=%s value=%s", req.command, req.value)

    if req.command not in ALLOWED_SYSTEM_COMMANDS:
        await log_event(f"system_blocked | {req.command} not allowed")
        raise HTTPException(
            status_code=403,
            detail=f"Command '{req.command}' is not in the allowed commands list. "
                   f"Allowed: {', '.join(ALLOWED_SYSTEM_COMMANDS)}",
        )

    try:
        result = execute_command(req.command, req.value)
        await log_event(
            f"system_execute | cmd={req.command} val={req.value} success={result.get('success')}"
        )

        return SystemCommandResponse(
            success=result.get("success", False),
            output=result.get("output", ""),
            error=result.get("error", ""),
        )

    except Exception as exc:
        log.error("System execute error: %s", exc)
        await log_event(f"system_error | {exc}")
        raise HTTPException(status_code=500, detail=f"Command execution failed: {exc}")
