"""
User persistence.

"""
from microcosm.api import binding
from microcosm_postgres.store import Store

from tweetthis.models.user import User


@binding("user_store")
class UserStore(Store):

    def __init__(self, graph):
        super().__init__(self, User)

    def retrieve_by_username(self, username):
        return self._retrieve(User.username == username)

    def _filter(
        self,
        query,
        username=None,
        email=None,
        first_name=None,
        last_name=None,
        **kwargs
    ):
        if username is not None:
            query = query.filter(
                User.username == username,
            )
        if email is not None:
            query = query.filter(
                User.email == email,
            )
        if first_name is not None:
            query = query.filter(
                User.first_name == first_name,
            )
        if last_name is not None:
            query = query.filter(
                User.last_name == last_name,
            )
        return super()._filter(query, **kwargs)

    def _order_by(self, query, **kwargs):
        return query.order_by(
            User.username.asc(),
        )
