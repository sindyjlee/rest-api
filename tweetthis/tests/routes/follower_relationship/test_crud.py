"""
Follower Relationship CRUD routes tests.

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
from tweetthis.models.follower_relationship import FollowerRelationship


class TestFollowerRelationshipRoutes:

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
            user_id=self.user1.id,
            follower_id=self.user2.id,
        )
        self.user2_follow_user1 = FollowerRelationship(
            id=new_object_id(),
            user_id=self.user2.id,
            follower_id=self.user1.id,
        )

    def teardown(self):
        self.graph.postgres.dispose()

    def test_search(self):
        with SessionContext(self.graph), transaction():
            self.user1_follow_user2.create()
            self.user2_follow_user1.create()

        uri = "/api/v1/follower_relationship"

        response = self.client.get(uri)

        assert_that(response.status_code, is_(equal_to(200)))
        data = loads(response.data)
        assert_that(len(data["items"]), is_(equal_to(2)))
        assert_that(data, has_entries(
            items=contains(
                has_entries(
                    id=str(self.user2_follow_user1.id),
                    userId=str(self.user2_follow_user1.user_id),
                    followerId=str(self.user2_follow_user1.follower_id),
                ),
                has_entries(
                    id=str(self.user1_follow_user2.id),
                    userId=str(self.user1_follow_user2.user_id),
                    followerId=str(self.user1_follow_user2.follower_id),
                ),
            ),
        ))

        response = self.client.get(
            uri,
            query_string=dict(
                follower_id=str(self.user1.id),
            ),
        )

        assert_that(response.status_code, is_(equal_to(200)))
        data = loads(response.data)
        assert_that(len(data["items"]), is_(equal_to(1)))
        assert_that(data, has_entries(
            items=contains(
                has_entries(
                    id=str(self.user2_follow_user1.id),
                    userId=str(self.user2_follow_user1.user_id),
                    followerId=str(self.user2_follow_user1.follower_id),
                ),
            ),
        ))

    def test_create(self):
        uri = "/api/v1/follower_relationship"

        with patch.object(self.graph.follower_relationship_store, "new_object_id") as mocked:
            mocked.return_value = self.user1_follow_user2.id
            response = self.client.post(uri, data=dumps({
                "userId": str(self.user1_follow_user2.user_id),
                "followerId": str(self.user1_follow_user2.follower_id),
            }))

        assert_that(response.status_code, is_(equal_to(201)))
        data = loads(response.data)
        assert_that(data, has_entries(
            id=str(self.user1_follow_user2.id),
            userId=str(self.user1_follow_user2.user_id),
            followerId=str(self.user1_follow_user2.follower_id),
        ))

    def test_retrieve(self):
        with SessionContext(self.graph), transaction():
            self.user1_follow_user2.create()

        uri = "/api/v1/follower_relationship/{}".format(self.user1_follow_user2.id)

        response = self.client.get(uri)

        data = loads(response.data)
        assert_that(data, has_entries(
            id=str(self.user1_follow_user2.id),
            userId=str(self.user1_follow_user2.user_id),
            followerId=str(self.user1_follow_user2.follower_id),
        ))

    def test_delete(self):
        with SessionContext(self.graph), transaction():
            self.user1_follow_user2.create()

        uri = "/api/v1/follower_relationship/{}".format(self.user1_follow_user2.id)

        response = self.client.delete(uri)
        assert_that(response.status_code, is_(equal_to(204)))
