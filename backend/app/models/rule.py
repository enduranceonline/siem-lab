from typing import Any, Optional
from sqlalchemy import Boolean, DateTime, Integer, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Rule(Base):
    __tablename__ = "rules"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="true")

    # criterios
    source: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    severity_min: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    contains: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)

    # throttle por regla (segundos)
    throttle_seconds: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # threshold: N eventos en X segundos
    threshold_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    threshold_seconds: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # match por meta
    meta_match: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, nullable=True)

    created_at: Mapped[object] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
