"""
User CRUD routes tests.

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


class TestUserRoutes:

    def setup(self):
        self.graph = create_app(testing=True)
        self.client = self.graph.flask.test_client()
        recreate_all(self.graph)

        self.username1 = "glen.runciter"
        self.email1 = "glen.runciter@runciter.com"
        self.first_name1 = "Glen"
        self.last_name1 = "Runciter"
        self.title1 = "Big Boss"
        self.bio1 = "Ubik-- get it today!"

        self.user1 = User(
            id=new_object_id(),
            username=self.username1,
            email=self.email1,
            first_name=self.first_name1,
            last_name=self.last_name1,
            title=self.title1,
            bio=self.bio1,
        )

    def teardown(self):
        self.graph.postgres.dispose()

    def test_search(self):
        self.username2 = "joe.chip"
        self.email2 = "joe.chip@runciter.com"
        self.first_name2 = "Joe"
        self.last_name2 = "Chip"
        self.title2 = "Technician"
        self.bio2 = "Ubik-- get it today!"

        self.user2 = User(
            id=new_object_id(),
            username=self.username2,
            email=self.email2,
            first_name=self.first_name2,
            last_name=self.last_name2,
            title=self.title2,
            bio=self.bio2,
        )

        with SessionContext(self.graph), transaction():
            self.user1.create()
            self.user2.create()

        uri = "/api/v1/user"

        response = self.client.get(uri)

        assert_that(response.status_code, is_(equal_to(200)))
        data = loads(response.data)
        assert_that(len(data["items"]), is_(equal_to(2)))
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

        response = self.client.get(
            uri,
            query_string=dict(
                username=self.user1.username,
            ),
        )

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

    def test_create(self):
        uri = "/api/v1/user"

        with patch.object(self.graph.user_store, "new_object_id") as mocked:
            mocked.return_value = self.user1.id
            response = self.client.post(uri, data=dumps({
                "username": self.user1.username,
                "email": self.user1.email,
                "firstName": self.user1.first_name,
                "lastName": self.user1.last_name,
                "title": self.user1.title,
                "bio": self.user1.bio,
            }))

        assert_that(response.status_code, is_(equal_to(201)))
        data = loads(response.data)
        assert_that(data, has_entries(
            id=str(self.user1.id),
            username=self.user1.username,
            email=self.user1.email,
            firstName=self.user1.first_name,
            lastName=self.user1.last_name,
            title=self.user1.title,
            bio=self.user1.bio,
        ))

    def test_update(self):
        with SessionContext(self.graph), transaction():
            self.user1.create()

        uri = "/api/v1/user/{}".format(self.user1.id)

        response = self.client.patch(uri, data=dumps({
            "firstName": self.user1.first_name,
            "lastName": self.user1.last_name,
            "title": self.user1.title,
            "bio": "A new bio!",
        }))

        assert_that(response.status_code, is_(equal_to(200)))
        data = loads(response.data)
        assert_that(data, has_entries(
            id=str(self.user1.id),
            username=self.user1.username,
            email=self.user1.email,
            firstName=self.user1.first_name,
            lastName=self.user1.last_name,
            title=self.user1.title,
            bio="A new bio!",
        ))

    def test_retrieve(self):
        with SessionContext(self.graph), transaction():
            self.user1.create()

        uri = "/api/v1/user/{}".format(self.user1.id)

        response = self.client.get(uri)

        data = loads(response.data)
        assert_that(data, has_entries(
            id=str(self.user1.id),
            username=self.user1.username,
            email=self.user1.email,
            firstName=self.user1.first_name,
            lastName=self.user1.last_name,
            title=self.user1.title,
            bio=self.user1.bio,
        ))

    def test_delete(self):
        with SessionContext(self.graph), transaction():
            self.user1.create()

        uri = "/api/v1/user/{}".format(self.user1.id)

        response = self.client.delete(uri)
        assert_that(response.status_code, is_(equal_to(204)))
