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
        """
        Sort by descending created date aka most recent first.

        """
        return query.order_by(
            FollowerRelationship.created_at.desc(),
        )

    def get_following_user_ids_by_user(self, user_id):
        """
        Return list of ids for users the given user is following.

        """
        # get all follower relationships where given user is follower
        following = self.search(follower_id=user_id)
        # return list of ids for users being followed by given user
        return [user.user_id for user in following]
