"""
Tweet model.

"""
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy_utils import UUIDType

from microcosm_postgres.models import EntityMixin, Model


class Tweet(EntityMixin, Model):
    __tablename__ = "tweet"

    user_id = Column(UUIDType, ForeignKey("user.id"), nullable=False)
    tweet_content = Column(String(280), nullable=False)
