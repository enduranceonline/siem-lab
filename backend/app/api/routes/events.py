from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.event import Event
from app.schemas.event import EventCreate, EventOut

router = APIRouter(prefix="/events", tags=["events"])


@router.post("", response_model=EventOut)
def create_event(payload: EventCreate, db: Session = Depends(get_db)):
    ev = Event(source=payload.source, severity=payload.severity, message=payload.message)
    db.add(ev)
    db.commit()
    db.refresh(ev)
    return ev


@router.get("", response_model=list[EventOut])
def list_events(
    limit: int = Query(50, ge=1, le=500),
    before_id: Optional[int] = Query(None, ge=1),
    source: Optional[str] = None,
    severity_min: Optional[int] = Query(None, ge=0, le=10),
    severity_max: Optional[int] = Query(None, ge=0, le=10),
    q: Optional[str] = None,
    meta_key: Optional[str] = None,
    meta_value: Optional[str] = None,
    db: Session = Depends(get_db),
):
    stmt = select(Event)

    if before_id is not None:
        stmt = stmt.where(Event.id < before_id)

    if source:
        stmt = stmt.where(Event.source == source)

    if severity_min is not None:
        stmt = stmt.where(Event.severity >= severity_min)

    if severity_max is not None:
        stmt = stmt.where(Event.severity <= severity_max)

    if q:
        stmt = stmt.where(Event.message.ilike(f"%{q}%"))

    if meta_key and meta_value:
        stmt = stmt.where(Event.meta[meta_key].astext == meta_value)
    elif meta_key:
        stmt = stmt.where(Event.meta.has_key(meta_key))  # noqa: W601

    stmt = stmt.order_by(Event.id.desc()).limit(limit)
    return db.execute(stmt).scalars().all()
