"""initial schema

Revision ID: 8cdfd9adfd92
Revises: 41ef381751e8
Create Date: 2025-09-13 14:23:28.899458

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8cdfd9adfd92'
down_revision: Union[str, Sequence[str], None] = '41ef381751e8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
