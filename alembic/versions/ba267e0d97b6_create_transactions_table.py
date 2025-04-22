"""create transactions table

Revision ID: ba267e0d97b6
Revises: 134e8d14e5ce
Create Date: 2025-04-22 04:42:51.196120

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ba267e0d97b6'
down_revision: Union[str, None] = '134e8d14e5ce'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create the transactions table
    transactions_table = op.create_table(
        'transactions',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('account_id', sa.Integer, sa.ForeignKey('accounts.id', ondelete='CASCADE'), nullable=False),
        sa.Column('amount', sa.Float, nullable=False),
        sa.Column('description', sa.String(200), nullable=True),
    )

    # Populate the transactions table
    op.bulk_insert(transactions_table,
    [
        {'id': 1, 'account_id': 1, 'amount': 100.50, 'description': 'Purchase at Store'},
        {'id': 2, 'account_id': 1, 'amount': 200.75, 'description': None},
        {'id': 3, 'account_id': 2, 'amount': 50.00, 'description': 'Online Subscription'},
    ])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('transactions')
