"""
User relation routes tests.

Tests are sunny day cases under the assumption that framework conventions
handle most error conditions.

"""
from json import loads

from hamcrest import (
    assert_that,
    contains,
    equal_to,
    has_entries,
    is_,
)
from microcosm_postgres.context import SessionContext, transaction
from microcosm_postgres.operations import recreate_all
from microcosm_postgres.identifiers import new_object_id

from tweetthis.app import create_app
from tweetthis.models.follower_relationship import FollowerRelationship
from tweetthis.models.tweet import Tweet
from tweetthis.models.user import User


class TestUserRelationRoutes:

    def setup(self):
        self.graph = create_app(testing=True)
        self.client = self.graph.flask.test_client()
        recreate_all(self.graph)

        self.username1 = "glen.runciter"
        self.user1 = User(
            username=self.username1,
            email="glen.runciter@runciter.com",
            first_name="Glen",
            last_name="Runciter",
            title="Big Boss",
            bio="Ubik-- get it today!",
        )

        self.username2 = "joe.chip"
        self.user2 = User(
            username=self.username2,
            email="joe.chip@runciter.com",
            first_name="Joe",
            last_name="Chip",
            title="Technician",
            bio="Ubik-- get it today!",
        )

        with SessionContext(self.graph), transaction():
            self.user1.create()
            self.user2.create()

        self.user1_follow_user2 = FollowerRelationship(
            id=new_object_id(),
            user_id=self.user2.id,
            follower_id=self.user1.id,
        )

        self.user2_tweet_content1 = """
            Friends, this is clean-up time and we’re discounting all our silent,
            electric Ubiks by this much money. Yes, we’re throwing away the blue-book.
            And remember: every Ubik on our lot has been used only as directed.
        """
        self.user2_tweet_content2 = """
            The best way to ask for beer is to sing out Ubik.
            Made from select hops, choice water, slow-aged for perfect flavor,
            Ubik is the nation’s number-one choice in beer. Made only in Cleveland.
        """

        with SessionContext(self.graph), transaction():
            self.user1_follow_user2.create()

            self.user2_tweet1 = Tweet(
                id=new_object_id(),
                user_id=self.user2.id,
                tweet_content=self.user2_tweet_content1,
            ).create()
            self.user2_tweet2 = Tweet(
                id=new_object_id(),
                user_id=self.user2.id,
                tweet_content=self.user2_tweet_content2,
            ).create()

    def teardown(self):
        self.graph.postgres.dispose()

    def test_search_following_by_user(self):
        uri = "/api/v1/user/{}/following".format(self.user1.id)

        response = self.client.get(uri)

        assert_that(response.status_code, is_(equal_to(200)))
        data = loads(response.data)
        assert_that(len(data["items"]), is_(equal_to(1)))
        assert_that(data, has_entries(
            items=contains(
                has_entries(
                    id=str(self.user2.id),
                    username=self.user2.username,
                    email=self.user2.email,
                    firstName=self.user2.first_name,
                    lastName=self.user2.last_name,
                    title=self.user2.title,
                    bio=self.user2.bio,
                ),
            ),
        ))

        uri = "/api/v1/user/{}/following".format(self.user2.id)

        response = self.client.get(uri)

        assert_that(response.status_code, is_(equal_to(200)))
        data = loads(response.data)
        assert_that(len(data["items"]), is_(equal_to(0)))

    def test_search_followers_by_user(self):
        uri = "/api/v1/user/{}/followers".format(self.user2.id)

        response = self.client.get(uri)

        assert_that(response.status_code, is_(equal_to(200)))
        data = loads(response.data)
        assert_that(len(data["items"]), is_(equal_to(1)))
        assert_that(data, has_entries(
            items=contains(
                has_entries(
                    id=str(self.user1.id),
                    username=self.user1.username,
                    email=self.user1.email,
                    firstName=self.user1.first_name,
                    lastName=self.user1.last_name,
                    title=self.user1.title,
                    bio=self.user1.bio,
                ),
            ),
        ))

        uri = "/api/v1/user/{}/followers".format(self.user1.id)

        response = self.client.get(uri)

        assert_that(response.status_code, is_(equal_to(200)))
        data = loads(response.data)
        assert_that(len(data["items"]), is_(equal_to(0)))

    def test_search_tweets_by_user(self):
        uri = "/api/v1/user/{}/tweets".format(self.user2.id)

        response = self.client.get(uri)

        assert_that(response.status_code, is_(equal_to(200)))
        data = loads(response.data)
        assert_that(len(data["items"]), is_(equal_to(2)))
        assert_that(data, has_entries(
            items=contains(
                has_entries(
                    id=str(self.user2_tweet2.id),
                    userId=str(self.user2_tweet2.user_id),
                    tweetContent=self.user2_tweet2.tweet_content,
                ),
                has_entries(
                    id=str(self.user2_tweet1.id),
                    userId=str(self.user2_tweet1.user_id),
                    tweetContent=self.user2_tweet1.tweet_content,
                ),
            ),
        ))

        uri = "/api/v1/user/{}/tweets".format(self.user1.id)

        response = self.client.get(uri)

        assert_that(response.status_code, is_(equal_to(200)))
        data = loads(response.data)
        assert_that(len(data["items"]), is_(equal_to(0)))

    def test_search_feed_by_user(self):
        uri = "/api/v1/user/{}/feed".format(self.user1.id)

        response = self.client.get(uri)

        assert_that(response.status_code, is_(equal_to(200)))
        data = loads(response.data)
        assert_that(len(data["items"]), is_(equal_to(2)))
        assert_that(data, has_entries(
            items=contains(
                has_entries(
                    id=str(self.user2_tweet2.id),
                    userId=str(self.user2_tweet2.user_id),
                    tweetContent=self.user2_tweet2.tweet_content,
                ),
                has_entries(
                    id=str(self.user2_tweet1.id),
                    userId=str(self.user2_tweet1.user_id),
                    tweetContent=self.user2_tweet1.tweet_content,
                ),
            ),
        ))

        uri = "/api/v1/user/{}/feed".format(self.user2.id)

        response = self.client.get(uri)

        assert_that(response.status_code, is_(equal_to(200)))
        data = loads(response.data)
        assert_that(len(data["items"]), is_(equal_to(0)))
