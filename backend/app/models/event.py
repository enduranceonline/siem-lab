from typing import Any, Optional
from sqlalchemy.dialects.postgresql import JSONB

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    ts: Mapped[object] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    source: Mapped[str] = mapped_column(String(64), nullable=False)
    severity: Mapped[int] = mapped_column(Integer, nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)

    created_at: Mapped[object] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    meta: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, nullable=True)

