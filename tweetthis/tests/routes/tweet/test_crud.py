"""
Tweet CRUD routes tests.

Tests are sunny day cases under the assumption that framework conventions
handle most error conditions.

"""
from json import dumps, loads

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
from mock import patch

from tweetthis.app import create_app
from tweetthis.models.user import User
from tweetthis.models.tweet import Tweet


class TestTweetRoutes:

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
        self.user1_tweet_content1 = """
            Friends, this is clean-up time and we’re discounting all our silent,
            electric Ubiks by this much money. Yes, we’re throwing away the blue-book.
            And remember: every Ubik on our lot has been used only as directed.
        """
        self.user1_tweet_content2 = """
            The best way to ask for beer is to sing out Ubik.
            Made from select hops, choice water, slow-aged for perfect flavor,
            Ubik is the nation’s number-one choice in beer. Made only in Cleveland.
        """

        self.username2 = "joe.chip"
        self.user2 = User(
            username=self.username2,
            email="joe.chip@runciter.com",
            first_name="Joe",
            last_name="Chip",
            title="Technician",
            bio="Ubik-- get it today!",
        )
        self.user2_tweet_content1 = """
            Instant Ubik has all the fresh flavor of just-brewed drip coffee.
            Your husband will say, Christ, Sally, I used to think your coffee was only so-so.
            But now, wow! Safe when taken as directed.
        """

        with SessionContext(self.graph), transaction():
            self.user1.create()
            self.user2.create()

        self.user1_tweet1 = Tweet(
            id=new_object_id(),
            user_id=self.user1.id,
            tweet_content=self.user1_tweet_content1,
        )
        self.user1_tweet2 = Tweet(
            id=new_object_id(),
            user_id=self.user1.id,
            tweet_content=self.user1_tweet_content2,
        )
        self.user2_tweet1 = Tweet(
            id=new_object_id(),
            user_id=self.user2.id,
            tweet_content=self.user2_tweet_content1,
        )

    def teardown(self):
        self.graph.postgres.dispose()

    def test_search(self):
        with SessionContext(self.graph), transaction():
            self.user1_tweet1.create()
            self.user1_tweet2.create()
            self.user2_tweet1.create()

        uri = "/api/v1/tweet"

        response = self.client.get(uri)

        assert_that(response.status_code, is_(equal_to(200)))
        data = loads(response.data)
        assert_that(len(data["items"]), is_(equal_to(3)))
        assert_that(data, has_entries(
            items=contains(
                has_entries(
                    id=str(self.user2_tweet1.id),
                    userId=str(self.user2_tweet1.user_id),
                    tweetContent=self.user2_tweet1.tweet_content,
                ),
                has_entries(
                    id=str(self.user1_tweet2.id),
                    userId=str(self.user1_tweet2.user_id),
                    tweetContent=self.user1_tweet2.tweet_content,
                ),
                has_entries(
                    id=str(self.user1_tweet1.id),
                    userId=str(self.user1_tweet1.user_id),
                    tweetContent=self.user1_tweet1.tweet_content,
                ),
            ),
        ))

        response = self.client.get(
            uri,
            query_string=dict(
                user_id=str(self.user1.id),
            ),
        )

        assert_that(response.status_code, is_(equal_to(200)))
        data = loads(response.data)
        assert_that(len(data["items"]), is_(equal_to(2)))
        assert_that(data, has_entries(
            items=contains(
                has_entries(
                    id=str(self.user1_tweet2.id),
                    userId=str(self.user1_tweet2.user_id),
                    tweetContent=self.user1_tweet2.tweet_content,
                ),
                has_entries(
                    id=str(self.user1_tweet1.id),
                    userId=str(self.user1_tweet1.user_id),
                    tweetContent=self.user1_tweet1.tweet_content,
                ),
            ),
        ))

    def test_create(self):
        uri = "/api/v1/tweet"

        with patch.object(self.graph.tweet_store, "new_object_id") as mocked:
            mocked.return_value = self.user1_tweet1.id
            response = self.client.post(uri, data=dumps({
                "userId": str(self.user1_tweet1.user_id),
                "tweetContent": self.user1_tweet1.tweet_content,
            }))

        assert_that(response.status_code, is_(equal_to(201)))
        data = loads(response.data)
        assert_that(data, has_entries(
            id=str(self.user1_tweet1.id),
            userId=str(self.user1_tweet1.user_id),
            tweetContent=self.user1_tweet1.tweet_content,
        ))

    def test_retrieve(self):
        with SessionContext(self.graph), transaction():
            self.user1_tweet1.create()

        uri = "/api/v1/tweet/{}".format(self.user1_tweet1.id)

        response = self.client.get(uri)

        data = loads(response.data)
        assert_that(data, has_entries(
            id=str(self.user1_tweet1.id),
            userId=str(self.user1_tweet1.user_id),
            tweetContent=self.user1_tweet1.tweet_content,
        ))

    def test_delete(self):
        with SessionContext(self.graph), transaction():
            self.user1_tweet1.create()

        uri = "/api/v1/tweet/{}".format(self.user1_tweet1.id)

        response = self.client.delete(uri)
        assert_that(response.status_code, is_(equal_to(204)))
