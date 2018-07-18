"""
User controller.

"""
from microcosm.api import binding
from microcosm_flask.conventions.crud_adapter import CRUDStoreAdapter
from microcosm_flask.namespaces import Namespace

from tweetthis.models.user import User


@binding("user_controller")
class UserController(CRUDStoreAdapter):

    def __init__(self, graph):
        super().__init__(graph, graph.user_store)
        self.follower_relationship_store = graph.follower_relationship_store
        self.tweet_controller = graph.tweet_controller

        self.ns = Namespace(
            subject=User,
            version="v1",
        )

        # list of users following given User
        self.followers_ns = Namespace(
            subject=User,
            object_="followers",
            version="v1",
        )

        # list of users given User is following
        self.following_ns = Namespace(
            subject=User,
            object_="following",
            version="v1",
        )

        # list of tweets posted by given User
        self.tweets_ns = Namespace(
            subject=User,
            object_="tweets",
            version="v1",
        )

        # list of tweets from users given User is following
        self.feed_ns = Namespace(
            subject=User,
            object_="feed",
            version="v1",
        )

    def search_following_by_user(
        self,
        user_id=None,
        offset=None,
        limit=None,
        **kwargs
    ):
        """
        Return list of users the given user is following.

        """
        # get list of ids for users being followed by given user
        user_id_list = self.follower_relationship_store.get_following_user_ids_by_user(user_id=user_id)

        # search + return users by user id list
        items = self.store.search(
            user_id_list=user_id_list,
            offset=offset,
            limit=limit,
            **kwargs
        )
        count = self.store.count(user_id_list=user_id_list, **kwargs)
        context = dict(user_id=user_id, user_id_list=user_id_list)
        return items, count, context

    def search_followers_by_user(
        self,
        user_id=None,
        offset=None,
        limit=None,
        **kwargs
    ):
        """
        Return list of following users aka followers for the given user.

        """
        # get all follower relationships where given user is user (being followed)
        followers = self.follower_relationship_store.search(user_id=user_id)
        # get list of ids for following users aka followers for given user
        user_id_list = [user.follower_id for user in followers]

        # search + return users by user id list
        items = self.store.search(
            user_id_list=user_id_list,
            offset=offset,
            limit=limit,
            **kwargs
        )
        count = self.store.count(user_id_list=user_id_list, **kwargs)
        context = dict(user_id=user_id, user_id_list=user_id_list)
        return items, count, context

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
        return self.tweet_controller.search_tweets_by_user(
            user_id=user_id,
            offset=offset,
            limit=limit,
            **kwargs
        )

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
        return self.tweet_controller.search_feed_by_user(
            user_id=user_id,
            offset=offset,
            limit=limit,
            **kwargs
        )
