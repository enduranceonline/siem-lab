from __future__ import annotations

import os
from datetime import datetime, timezone

from fastapi import APIRouter

router = APIRouter(prefix="/info", tags=["info"])


@router.get("")
def info():
    return {
        "name": "siem-backend",
        "version": os.getenv("APP_VERSION", "0.1.0"),
        "git_sha": os.getenv("GIT_SHA", "unknown"),
        "build_time": os.getenv("BUILD_TIME", "unknown"),
        "utc_now": datetime.now(timezone.utc).isoformat(),
    }
