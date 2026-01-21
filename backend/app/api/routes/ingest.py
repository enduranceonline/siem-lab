from __future__ import annotations

from datetime import datetime, timezone, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.alert import Alert
from app.models.event import Event
from app.models.rule import Rule
from app.schemas.event import EventOut
from app.schemas.ingest import IngestPayload

router = APIRouter(prefix="/ingest", tags=["ingest"])


def _compute_group_key(ev: Event) -> str | None:
    if not ev.meta:
        return None
    return ev.meta.get("host")


@router.post("", response_model=EventOut)
def ingest(payload: IngestPayload, db: Session = Depends(get_db)):
    now = datetime.now(timezone.utc)

    try:
        # 1) Guardar evento
        ev = Event(
            ts=now,
            source=payload.source,
            severity=payload.severity,
            message=payload.message,
            meta=payload.meta,
        )
        db.add(ev)
        db.flush()  # ev.id disponible

        group_key = _compute_group_key(ev)

        # 2) Evaluar reglas habilitadas
        rules = db.execute(
            select(Rule).where(Rule.enabled.is_(True)).order_by(Rule.id.asc())
        ).scalars().all()

        for rule in rules:
            # 2.1 Source
            if rule.source and ev.source != rule.source:
                continue

            # 2.2 Severity
            if rule.severity_min is not None and ev.severity < rule.severity_min:
                continue

            # 2.3 Contains
            if rule.contains and rule.contains.lower() not in (ev.message or "").lower():
                continue

            # 2.4 Meta match exacto
            if rule.meta_match:
                if not ev.meta:
                    continue
                if any(ev.meta.get(k) != v for k, v in rule.meta_match.items()):
                    continue

            # 3) Throttle (ignorando closed)
            # Decisión: si group_key es None, NO aplicamos throttle (no hay agrupación fiable)
            if (
                group_key is not None
                and rule.throttle_seconds is not None
                and rule.throttle_seconds > 0
            ):
                last_alert_ts = (
                    db.execute(
                        select(Alert.created_at)
                        .where(
                            Alert.rule_id == rule.id,
                            Alert.group_key == group_key,
                            Alert.status.in_(("open", "ack")),
                        )
                        .order_by(Alert.created_at.desc())
                        .limit(1)
                    )
                    .scalar_one_or_none()
                )
                if last_alert_ts:
                    delta = (now - last_alert_ts).total_seconds()
                    if delta < rule.throttle_seconds:
                        continue

            # 3.5) Anti-duplicado (si hay open/ack, no crear otra)
            # Decisión: si group_key es None, NO aplicamos anti-duplicado (no hay agrupación fiable)
            if group_key is not None:
                existing_active_alert_id = (
                    db.execute(
                        select(Alert.id)
                        .where(
                            Alert.rule_id == rule.id,
                            Alert.group_key == group_key,
                            Alert.status.in_(("open", "ack")),
                        )
                        .order_by(Alert.created_at.desc())
                        .limit(1)
                    )
                    .scalar_one_or_none()
                )
                if existing_active_alert_id is not None:
                    continue

            # 4) Threshold
            if rule.threshold_count is not None and rule.threshold_seconds is not None:
                if group_key is None:
                    continue

                window_start = now - timedelta(seconds=rule.threshold_seconds)
                stmt = select(func.count(Event.id)).where(Event.ts >= window_start)

                if rule.source:
                    stmt = stmt.where(Event.source == rule.source)

                if rule.severity_min is not None:
                    stmt = stmt.where(Event.severity >= rule.severity_min)

                if rule.contains:
                    stmt = stmt.where(Event.message.ilike(f"%{rule.contains}%"))

                if rule.meta_match:
                    stmt = stmt.where(Event.meta.contains(rule.meta_match))

                stmt = stmt.where(Event.meta.contains({"host": group_key}))

                matched_count = db.execute(stmt).scalar_one()
                if matched_count < rule.threshold_count:
                    continue

            # 5) Crear alerta
            alert = Alert(
                rule_id=rule.id,
                event_id=ev.id,
                title=f"Rule matched: {rule.name}",
                group_key=group_key,
            )
            db.add(alert)

        db.commit()
        return ev

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Ingest failed") from e
