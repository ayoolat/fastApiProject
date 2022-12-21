"""first migration

Revision ID: 00eba210eaf2
Revises: c21ddeaf4a2e
Create Date: 2022-12-15 10:05:57.441491

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '00eba210eaf2'
down_revision = 'c21ddeaf4a2e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
