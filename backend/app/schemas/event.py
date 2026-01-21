from typing import Any, Optional

from datetime import datetime
from pydantic import BaseModel, Field


class EventCreate(BaseModel):
    source: str = Field(min_length=1, max_length=64)
    severity: int = Field(ge=0, le=10)
    message: str = Field(min_length=1)


class EventOut(BaseModel):
    id: int
    ts: datetime
    source: str
    severity: int
    message: str
    meta: Optional[dict[str, Any]] = None
    created_at: datetime
 
    model_config = {"from_attributes": True}
