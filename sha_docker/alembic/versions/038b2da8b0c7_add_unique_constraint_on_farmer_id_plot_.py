"""add unique constraint on farmer_id_plot_no_survey_no

Revision ID: 038b2da8b0c7
Revises: d75b2fe95a5b
Create Date: 2025-11-03 12:16:13.498704

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '038b2da8b0c7'
down_revision: Union[str, Sequence[str], None] = 'd75b2fe95a5b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(
        'uq_farmer_plot_survey',
        'land_parcel',
        ['farmer_id', 'plot_no', 'survey_no']
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        'uq_farmer_plot_survey',
        'land_parcel',
        type_='unique'
    )