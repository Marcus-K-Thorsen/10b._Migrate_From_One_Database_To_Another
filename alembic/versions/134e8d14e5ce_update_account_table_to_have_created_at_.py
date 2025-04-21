"""update account table to have created at column

Revision ID: 134e8d14e5ce
Revises: aa5687d9b2c6
Create Date: 2025-04-21 10:01:21.727095

"""
from typing import Sequence, Union
from datetime import date

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '134e8d14e5ce'
down_revision: Union[str, None] = 'aa5687d9b2c6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'accounts',
        sa.Column('created_at', sa.Date(), nullable=True),
    )
    
    today = date(2025, 4, 11)
    op.execute(
        f"UPDATE accounts SET created_at = '{today}'"
    )
    
    op.alter_column(
        'accounts',
        'created_at',
        existing_type=sa.Date(),
        nullable=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Remove the column
    op.drop_column('accounts', 'created_at')

