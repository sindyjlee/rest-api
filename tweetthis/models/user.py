"""
User model.

"""
from sqlalchemy import Column, String

from microcosm_postgres.models import EntityMixin, Model


class User(EntityMixin, Model):
    __tablename__ = "user"

    username = Column(String(255), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    title = Column(String(255), nullable=True)
    bio = Column(String(255), nullable=True)
