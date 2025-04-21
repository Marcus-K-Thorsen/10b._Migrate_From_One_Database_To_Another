"""create account table

Revision ID: aa5687d9b2c6
Revises: 
Create Date: 2025-04-21 09:53:22.583976

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aa5687d9b2c6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    accounts_table = op.create_table(
        'accounts',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('description', sa.Unicode(200)),
    )
    op.bulk_insert(accounts_table,
    [
        {'name': 'John Smith', 'description': 'CEO'},
        {'name': 'Ed Williams', 'description': 'CTO'},
        {'name': 'Wendy Jones', 'description': 'CFO'},
    ])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('accounts')
