"""
Tweet persistence tests.

Tests cover model-specific constraints under the assumption that framework
conventions handle most boilerplate.

"""
from hamcrest import (
    assert_that,
    equal_to,
    is_,
)
from microcosm_postgres.context import SessionContext, transaction

from tweetthis.app import create_app
from tweetthis.models.user import User
from tweetthis.models.tweet import Tweet


class TestTweet:

    def setup(self):
        self.graph = create_app(testing=True)
        self.tweet_store = self.graph.tweet_store
        self.user_store = self.graph.user_store

        self.username = "joe.chip"
        self.user = User(
            username=self.username,
            email="joe.chip@runciter.com",
            first_name="Joe",
            last_name="Chip",
            title="Technician",
            bio="Ubik-- get it today!",
        )

        self.context = SessionContext(self.graph)
        self.context.recreate_all()
        self.context.open()

        with transaction():
            self.user_store.create(self.user)

        self.tweet_content = """
            Friends, this is clean-up time and we’re discounting all our silent,
            electric Ubiks by this much money. Yes, we’re throwing away the blue-book.
            And remember: every Ubik on our lot has been used only as directed.
        """

        self.tweet = Tweet(
            user_id=self.user.id,
            tweet_content=self.tweet_content,
        )

    def teardown(self):
        self.context.close()
        self.graph.postgres.dispose()

    def test_create(self):
        with transaction():
            self.tweet_store.create(self.tweet)

        retrieved_tweet = self.tweet_store.retrieve(self.tweet.id)
        assert_that(retrieved_tweet, is_(equal_to(self.tweet)))
