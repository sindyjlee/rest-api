"""
Add Follower Relationship model

Revision ID: e6e46ac86cff
Revises: f96c8e4abc04
Create Date: 2018-07-18 03:01:04.158067

"""
from alembic import op
from microcosm_postgres.models import UTCDateTime
from sqlalchemy import Column, ForeignKeyConstraint, PrimaryKeyConstraint
from sqlalchemy_utils import UUIDType


# revision identifiers, used by Alembic.
revision = 'e6e46ac86cff'
down_revision = 'f96c8e4abc04'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('follower_relationship',
        Column('id', UUIDType, nullable=False),
        Column('created_at', UTCDateTime(), nullable=False),
        Column('updated_at', UTCDateTime(), nullable=False),
        Column('user_id', UUIDType, nullable=True),
        Column('follower_id', UUIDType, nullable=True),
        ForeignKeyConstraint(['follower_id'], ['user.id'], ),
        ForeignKeyConstraint(['user_id'], ['user.id'], ),
        PrimaryKeyConstraint('id')
    )
    op.create_index('follower_relationship_by_user_id_follower_id', 'follower_relationship', ['user_id', 'follower_id'], unique=True)


def downgrade():
    op.drop_index('follower_relationship_by_user_id_follower_id', table_name='follower')
    op.drop_table('follower_relationship')
