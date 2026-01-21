from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


class RuleCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    enabled: bool = True
    source: Optional[str] = Field(default=None, max_length=64)
    severity_min: Optional[int] = Field(default=None, ge=0, le=10)
    contains: Optional[str] = Field(default=None, max_length=200)

    # throttle por regla (segundos)
    # None => usar DEFAULT_THROTTLE_SECONDS en el motor
    # 0    => sin throttle (alertar siempre)
    throttle_seconds: Optional[int] = Field(default=None, ge=0, le=86400)

    # threshold: dispara alerta cuando hay N eventos que matchean en X segundos
    threshold_count: Optional[int] = Field(default=None, ge=1, le=100000)
    threshold_seconds: Optional[int] = Field(default=None, ge=1, le=86400)

    # match por meta (exacto). Ej: {"host":"kali","facility":"auth"}
    meta_match: Optional[dict[str, Any]] = None


class RuleOut(BaseModel):
    id: int
    name: str
    enabled: bool
    source: Optional[str]
    severity_min: Optional[int]
    contains: Optional[str]

    throttle_seconds: Optional[int]
    threshold_count: Optional[int]
    threshold_seconds: Optional[int]

    meta_match: Optional[dict[str, Any]]
    created_at: datetime

    model_config = {"from_attributes": True}
