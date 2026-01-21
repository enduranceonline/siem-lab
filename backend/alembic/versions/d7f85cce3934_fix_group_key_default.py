"""fix group_key default

Revision ID: d7f85cce3934
Revises: 2e15d222277a
Create Date: 2026-01-16 12:20:45.616108
"""
from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d7f85cce3934"
down_revision: Union[str, Sequence[str], None] = "2e15d222277a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Quitar default '' y permitir NULL.
    # Además, alinear el tipo a VARCHAR(120) (tu modelo actual).
    op.alter_column(
        "alerts",
        "group_key",
        existing_type=sa.String(length=120),
        type_=sa.String(length=120),
        nullable=True,
        server_default=None,
    )


def downgrade() -> None:
    # Volver al estado anterior (NOT NULL + default '')
    # OJO: si existen NULLs, esto fallará. Por eso, antes forzamos ''.
    op.execute("UPDATE alerts SET group_key = '' WHERE group_key IS NULL")

    op.alter_column(
        "alerts",
        "group_key",
        existing_type=sa.String(length=120),
        type_=sa.String(length=120),
        nullable=False,
        server_default="",
    )
