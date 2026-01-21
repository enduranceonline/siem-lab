from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.alert import Alert
from app.models.event import Event
from app.models.rule import Rule

router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.get("")
def get_metrics(
    top_groups: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    events_total = db.execute(select(func.count()).select_from(Event)).scalar_one()
    rules_total = db.execute(select(func.count()).select_from(Rule)).scalar_one()
    rules_enabled = db.execute(
        select(func.count()).select_from(Rule).where(Rule.enabled.is_(True))
    ).scalar_one()
    alerts_total = db.execute(select(func.count()).select_from(Alert)).scalar_one()

    rows_status = db.execute(
        select(Alert.status, func.count())
        .group_by(Alert.status)
        .order_by(func.count().desc())
    ).all()
    alerts_by_status = {status: count for status, count in rows_status}

    rows_group = db.execute(
        select(Alert.group_key, func.count())
        .where(Alert.group_key.is_not(None))
        .group_by(Alert.group_key)
        .order_by(func.count().desc())
        .limit(top_groups)
    ).all()
    alerts_by_group_key = {group_key: count for group_key, count in rows_group}

    return {
        "events_total": events_total,
        "rules_total": rules_total,
        "rules_enabled": rules_enabled,
        "alerts_total": alerts_total,
        "alerts_by_status": alerts_by_status,
        "alerts_by_group_key_top": alerts_by_group_key,
    }
