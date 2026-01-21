from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Alert(Base):
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    rule_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("rules.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    event_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("events.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(String(200), nullable=False)

    # Agrupación (p.ej. host) para threshold/throttle por “grupo”
    group_key: Mapped[str | None] = mapped_column(String(120), nullable=True, index=True)

    # Ciclo de vida de la alerta (en SOC real esto es básico)
    # open  -> alerta nueva
    # ack   -> reconocida
    # closed-> cerrada
    status: Mapped[str] = mapped_column(String(16), nullable=False, server_default="open", index=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Relaciones (no obligatorias para el MVP, pero útiles)
    rule = relationship("Rule")
    event = relationship("Event")


# Índices adicionales (además de los index=True)
Index("ix_alerts_rule_id_created_at", Alert.rule_id, Alert.created_at)
Index("ix_alerts_group_key_created_at", Alert.group_key, Alert.created_at)
