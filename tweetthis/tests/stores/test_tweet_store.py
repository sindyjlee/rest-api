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

    def test_search_by_username(self):
        with transaction():
            self.tweet_store.create(self.tweet)

        other_user = User(
            username="glen.runciter",
            email="glen.runciter@runciter.com",
            first_name="Glen",
            last_name="Runciter",
            title="Big Boss",
            bio="",
        )
        other_tweet_content = """
            The best way to ask for beer is to sing out Ubik.
            Made from select hops, choice water, slow-aged for perfect flavor,
            Ubik is the nation’s number-one choice in beer. Made only in Cleveland.
        """

        with transaction():
            self.user_store.create(other_user)

            self.tweet_store.create(Tweet(
                user_id=other_user.id,
                tweet_content=other_tweet_content,
            ))

        retrieved_tweets = self.tweet_store.search_by_username(
            self.username
        )

        assert_that(len(retrieved_tweets), is_(equal_to(1)))
        assert_that(retrieved_tweets[0], is_(equal_to(self.tweet)))
