"""
Follower persistence.

"""
from microcosm.api import binding
from microcosm_postgres.store import Store

from tweetthis.models.follower_relationship import FollowerRelationship


@binding("follower_relationship_store")
class FollowerRelationshipStore(Store):

    def __init__(self, graph):
        super().__init__(self, FollowerRelationship)

    def _filter(
        self,
        query,
        user_id=None,
        follower_id=None,
        **kwargs
    ):
        if user_id is not None:
            query = query.filter(
                FollowerRelationship.user_id == user_id,
            )
        if follower_id is not None:
            query = query.filter(
                FollowerRelationship.follower_id == follower_id,
            )
        return super()._filter(query, **kwargs)

    def _order_by(self, query, **kwargs):
        return query.order_by(
            FollowerRelationship.created_at.desc(),
        )
