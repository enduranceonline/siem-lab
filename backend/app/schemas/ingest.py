from pydantic import BaseModel, Field
from typing import Optional, Any


class IngestPayload(BaseModel):
    source: str = Field(min_length=1, max_length=64)
    severity: int = Field(ge=0, le=10)
    message: str = Field(min_length=1)

    # opcional: para futuro (IP, host, raw, etc.)
    meta: Optional[dict[str, Any]] = None
