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

    def _filter(
        self,
        query,
        user_id=None,
        tweet_content_substring=None,
        user_id_list=None,
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
        if user_id_list is not None:
            query = query.filter(
                Tweet.user_id.in_(user_id_list)
            )
        return super()._filter(query, **kwargs)

    def _order_by(self, query, **kwargs):
        """
        Sort tweets by descending created date aka most recent first.

        """
        return query.order_by(
            Tweet.created_at.desc(),
        )
