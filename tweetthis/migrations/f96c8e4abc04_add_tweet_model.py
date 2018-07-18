"""
Add Tweet model

Revision ID: f96c8e4abc04
Revises: 4a68ff6f9e11
Create Date: 2018-07-18 00:36:41.290158

"""
from alembic import op
from microcosm_postgres.models import UTCDateTime
from sqlalchemy import (
    Column,
    ForeignKeyConstraint,
    PrimaryKeyConstraint,
    String,
    UniqueConstraint,
)
from sqlalchemy_utils import UUIDType


# revision identifiers, used by Alembic.
revision = 'f96c8e4abc04'
down_revision = '4a68ff6f9e11'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('tweet',
        Column('id', UUIDType, nullable=False),
        Column('created_at', UTCDateTime(), nullable=False),
        Column('updated_at', UTCDateTime(), nullable=False),
        Column('user_id', UUIDType, nullable=False),
        Column('tweet_content', String(length=280), nullable=False),
        ForeignKeyConstraint(['user_id'], ['user.id'], ),
        PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('tweet')
