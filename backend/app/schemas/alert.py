from __future__ import annotations

from datetime import datetime
from typing import Optional, Literal

from pydantic import BaseModel, Field


AlertStatus = Literal["open", "ack", "closed"]


class AlertOut(BaseModel):
    id: int
    rule_id: int
    event_id: int
    title: str

    group_key: Optional[str] = None
    status: AlertStatus

    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class AlertUIOut(AlertOut):
    # Campos extra “listos para UI” (sin tocar BD)
    rule_name: str
    event_ts: datetime
    event_source: str
    event_severity: int
    event_message: str


class AlertUpdate(BaseModel):
    # Permitimos solo cambios de estado en el MVP
    status: AlertStatus = Field(...)
