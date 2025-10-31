"""add unique constraint on farmer_id and plot_no

Revision ID: 842a7abc5756
Revises: d64d5bfa6473
Create Date: 2025-10-30 13:17:35.832282
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '842a7abc5756'
down_revision: Union[str, Sequence[str], None] = 'd64d5bfa6473'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(
        "uq_farmer_plot",        # name of the constraint
        "land_parcel",           # name of the table
        ["farmer_id", "plot_no"] # columns to make unique together
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "uq_farmer_plot",
        "land_parcel",
        type_="unique"
    )
