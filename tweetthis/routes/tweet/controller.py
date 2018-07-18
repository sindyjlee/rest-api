"""
Tweet controller.

"""
from microcosm.api import binding
from microcosm_flask.conventions.crud_adapter import CRUDStoreAdapter
from microcosm_flask.namespaces import Namespace

from tweetthis.models.tweet import Tweet


@binding("tweet_controller")
class TweetController(CRUDStoreAdapter):

    def __init__(self, graph):
        super().__init__(graph, graph.tweet_store)
        self.follower_relationship_store = graph.follower_relationship_store

        self.ns = Namespace(
            subject=Tweet,
            version="v1",
        )

    def search_tweets_by_user(
        self,
        user_id=None,
        offset=None,
        limit=None,
        **kwargs
    ):
        """
        Return tweets posted by the given user.

        """
        items = self.store.search(
            user_id=user_id,
            offset=offset,
            limit=limit,
            **kwargs
        )
        count = self.store.count(user_id=user_id, **kwargs)
        context = dict(user_id=user_id)
        return items, count, context

    def search_feed_by_user(
        self,
        user_id=None,
        offset=None,
        limit=None,
        **kwargs
    ):
        """
        Return tweets posted by users the given user is following.

        """
        # get list of ids for users being followed by given user
        user_id_list = self.follower_relationship_store.get_following_user_ids_by_user(user_id=user_id)

        items = self.store.search(
            user_id_list=user_id_list,
            offset=offset,
            limit=limit,
            **kwargs
        )
        count = self.store.count(user_id_list=user_id_list, **kwargs)
        context = dict(user_id=user_id, user_id_list=user_id_list)
        return items, count, context
