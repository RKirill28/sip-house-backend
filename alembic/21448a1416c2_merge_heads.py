"""merge_heads

Revision ID: 21448a1416c2
Revises: 409146ea26ff, c75308f87805
Create Date: 2026-01-25 14:24:42.502496

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '21448a1416c2'
down_revision: Union[str, Sequence[str], None] = ('409146ea26ff', 'c75308f87805')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
