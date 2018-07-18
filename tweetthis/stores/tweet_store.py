"""
Tweet persistence.

"""
from microcosm.api import binding
from microcosm_postgres.store import Store

from tweetthis.models.tweet import Tweet


@binding("tweet_store")
class TweetStore(Store):

    def __init__(self, graph):
        super().__init__(self, Tweet)
        self.user_store = graph.user_store

    def search_by_username(self, username):
        user = self.user_store.retrieve_by_username(username)
        return self.search(user_id=user.id)

    def _filter(
        self,
        query,
        user_id=None,
        tweet_content_substring=None,
        **kwargs
    ):
        if user_id is not None:
            query = query.filter(
                Tweet.user_id == user_id,
            )
        if tweet_content_substring is not None:
            query = query.filter(
                Tweet.tweet_content.contains(tweet_content_substring),
            )
        return super()._filter(query, **kwargs)

    def _order_by(self, query, **kwargs):
        return query.order_by(
            Tweet.created_at.desc(),
        )
