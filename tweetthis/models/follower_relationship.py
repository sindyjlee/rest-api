"""
Follower Relationship model.

"""
from microcosm_postgres.models import Model, EntityMixin
from sqlalchemy import Column, ForeignKey, Index
from sqlalchemy_utils import UUIDType


class FollowerRelationship(Model, EntityMixin):
    __tablename__ = "follower_relationship"

    user_id = Column(UUIDType, ForeignKey('user.id'))
    follower_id = Column(UUIDType, ForeignKey('user.id'))

    __table_args__ = (
        Index(
            "follower_relationship_by_user_id_follower_id",
            "user_id",
            "follower_id",
            unique=True,
        ),
    )
