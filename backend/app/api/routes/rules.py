# backend/app/api/routes/rules.py

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.rule import Rule
from app.schemas.rule import RuleCreate, RuleOut

router = APIRouter(prefix="/rules", tags=["rules"])


@router.post("", response_model=RuleOut)
def create_rule(payload: RuleCreate, db: Session = Depends(get_db)):
    rule = Rule(
        name=payload.name,
        enabled=payload.enabled,
        source=payload.source,
        severity_min=payload.severity_min,
        contains=payload.contains,
        meta_match=payload.meta_match,
        throttle_seconds=payload.throttle_seconds,
        threshold_count=payload.threshold_count,
        threshold_seconds=payload.threshold_seconds,
    )

    db.add(rule)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Rule name already exists")

    db.refresh(rule)
    return rule


@router.get("", response_model=list[RuleOut])
def list_rules(
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    stmt = select(Rule).order_by(Rule.id.desc()).limit(limit)
    return db.execute(stmt).scalars().all()
