from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func, or_
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.alert import Alert
from app.models.event import Event
from app.models.rule import Rule
from app.schemas.alert import AlertOut, AlertUIOut, AlertUpdate, AlertStatus

router = APIRouter(prefix="/alerts", tags=["alerts"])


def _apply_ui_filters(
    stmt,
    *,
    status: AlertStatus | None,
    group_key: str | None,
    rule_id: int | None,
    severity_min: int | None,
    severity_max: int | None,
    source: str | None,
    q: str | None,
):
    if status:
        stmt = stmt.where(Alert.status == status)
    if group_key:
        stmt = stmt.where(Alert.group_key == group_key)
    if rule_id is not None:
        stmt = stmt.where(Alert.rule_id == rule_id)
    if severity_min is not None:
        stmt = stmt.where(Event.severity >= severity_min)
    if severity_max is not None:
        stmt = stmt.where(Event.severity <= severity_max)
    if source:
        # exact match pero case-insensitive
        stmt = stmt.where(func.lower(Event.source) == source.lower())
    if q:
        like = f"%{q}%"
        stmt = stmt.where(or_(Alert.title.ilike(like), Event.message.ilike(like)))
    return stmt


@router.get("", response_model=list[AlertOut])
def list_alerts(
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    status: AlertStatus | None = Query(None, description="Filter by status (open/ack/closed)"),
    group_key: str | None = Query(None, description="Filter by group_key (e.g. host)"),
    rule_id: int | None = Query(None, description="Filter by rule_id"),
    db: Session = Depends(get_db),
):
    stmt = select(Alert).order_by(Alert.created_at.desc()).limit(limit).offset(offset)

    if status:
        stmt = stmt.where(Alert.status == status)
    if group_key:
        stmt = stmt.where(Alert.group_key == group_key)
    if rule_id is not None:
        stmt = stmt.where(Alert.rule_id == rule_id)

    return db.execute(stmt).scalars().all()


@router.get("/ui", response_model=list[AlertUIOut])
def list_alerts_ui(
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    status: AlertStatus | None = Query(None, description="Filter by status (open/ack/closed)"),
    group_key: str | None = Query(None, description="Filter by group_key (e.g. host)"),
    rule_id: int | None = Query(None, description="Filter by rule_id"),
    severity_min: int | None = Query(None, ge=0, le=10, description="Filter by event severity >= severity_min"),
    severity_max: int | None = Query(None, ge=0, le=10, description="Filter by event severity <= severity_max"),
    source: str | None = Query(None, description="Filter by event source (case-insensitive exact match)"),
    q: str | None = Query(None, min_length=1, max_length=200, description="Search in title/event_message (case-insensitive)"),
    db: Session = Depends(get_db),
):
    if severity_min is not None and severity_max is not None and severity_min > severity_max:
        raise HTTPException(status_code=422, detail="severity_min cannot be greater than severity_max")

    stmt = (
        select(
            Alert,
            Rule.name.label("rule_name"),
            Event.ts.label("event_ts"),
            Event.source.label("event_source"),
            Event.severity.label("event_severity"),
            Event.message.label("event_message"),
        )
        .join(Rule, Rule.id == Alert.rule_id)
        .join(Event, Event.id == Alert.event_id)
        .order_by(Alert.created_at.desc())
        .limit(limit)
        .offset(offset)
    )

    stmt = _apply_ui_filters(
        stmt,
        status=status,
        group_key=group_key,
        rule_id=rule_id,
        severity_min=severity_min,
        severity_max=severity_max,
        source=source,
        q=q,
    )

    rows = db.execute(stmt).all()

    out: list[AlertUIOut] = []
    for alert, rule_name, event_ts, event_source, event_severity, event_message in rows:
        out.append(
            AlertUIOut(
                **AlertOut.model_validate(alert).model_dump(),
                rule_name=rule_name,
                event_ts=event_ts,
                event_source=event_source,
                event_severity=event_severity,
                event_message=event_message,
            )
        )
    return out


@router.get("/ui/count", response_model=int)
def count_alerts_ui(
    status: AlertStatus | None = Query(None),
    group_key: str | None = Query(None),
    rule_id: int | None = Query(None),
    severity_min: int | None = Query(None, ge=0, le=10),
    severity_max: int | None = Query(None, ge=0, le=10),
    source: str | None = Query(None),
    q: str | None = Query(None, min_length=1, max_length=200),
    db: Session = Depends(get_db),
):
    if severity_min is not None and severity_max is not None and severity_min > severity_max:
        raise HTTPException(status_code=422, detail="severity_min cannot be greater than severity_max")

    stmt = (
        select(func.count())
        .select_from(Alert)
        .join(Rule, Rule.id == Alert.rule_id)
        .join(Event, Event.id == Alert.event_id)
    )

    stmt = _apply_ui_filters(
        stmt,
        status=status,
        group_key=group_key,
        rule_id=rule_id,
        severity_min=severity_min,
        severity_max=severity_max,
        source=source,
        q=q,
    )

    return int(db.execute(stmt).scalar_one())


@router.get("/{alert_id}", response_model=AlertOut)
def get_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.get(Alert, alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert


@router.get("/{alert_id}/ui", response_model=AlertUIOut)
def get_alert_ui(alert_id: int, db: Session = Depends(get_db)):
    stmt = (
        select(
            Alert,
            Rule.name.label("rule_name"),
            Event.ts.label("event_ts"),
            Event.source.label("event_source"),
            Event.severity.label("event_severity"),
            Event.message.label("event_message"),
        )
        .join(Rule, Rule.id == Alert.rule_id)
        .join(Event, Event.id == Alert.event_id)
        .where(Alert.id == alert_id)
        .limit(1)
    )

    row = db.execute(stmt).first()
    if not row:
        raise HTTPException(status_code=404, detail="Alert not found")

    alert, rule_name, event_ts, event_source, event_severity, event_message = row

    return AlertUIOut(
        **AlertOut.model_validate(alert).model_dump(),
        rule_name=rule_name,
        event_ts=event_ts,
        event_source=event_source,
        event_severity=event_severity,
        event_message=event_message,
    )


@router.patch("/{alert_id}", response_model=AlertOut)
def update_alert(alert_id: int, payload: AlertUpdate, db: Session = Depends(get_db)):
    try:
        alert = db.get(Alert, alert_id)
        if not alert:
            raise HTTPException(status_code=404, detail="Alert not found")

        alert.status = payload.status
        db.add(alert)
        db.commit()
        db.refresh(alert)
        return alert

    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Update alert failed") from e
