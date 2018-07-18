"""
Add User model

Revision ID: 4a68ff6f9e11
Revises: e107ab9eb193
Create Date: 2018-07-17 21:30:24.887803

"""
from alembic import op
from microcosm_postgres.models import UTCDateTime
from sqlalchemy import Column, PrimaryKeyConstraint, String, UniqueConstraint
from sqlalchemy_utils import UUIDType

# revision identifiers, used by Alembic.
revision = '4a68ff6f9e11'
down_revision = 'e107ab9eb193'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('user',
        Column('id', UUIDType, nullable=False),
        Column('created_at', UTCDateTime(), nullable=False),
        Column('updated_at', UTCDateTime(), nullable=False),
        Column('username', String(length=255), nullable=False),
        Column('email', String(length=255), nullable=False),
        Column('first_name', String(length=255), nullable=False),
        Column('last_name', String(length=255), nullable=False),
        Column('title', String(length=255), nullable=True),
        Column('bio', String(length=255), nullable=True),
        PrimaryKeyConstraint('id'),
        UniqueConstraint('email'),
        UniqueConstraint('username')
    )


def downgrade():
    op.drop_table('user')
