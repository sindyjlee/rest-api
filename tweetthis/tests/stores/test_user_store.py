"""
User persistence tests.

Tests cover model-specific constraints under the assumption that framework
conventions handle most boilerplate.

"""
from hamcrest import (
    assert_that,
    calling,
    equal_to,
    is_,
    raises,
)
from microcosm_postgres.context import SessionContext, transaction
from microcosm_postgres.errors import DuplicateModelError

from tweetthis.app import create_app
from tweetthis.models.user import User


class TestUser:

    def setup(self):
        self.graph = create_app(testing=True)
        self.user_store = self.graph.user_store

        self.username = "joe.chip"
        self.email = "joe.chip@runciter.com"
        self.first_name = "Joe"
        self.last_name = "Chip"
        self.title = "Technician"
        self.bio = "Ubik-- get it today!"

        self.context = SessionContext(self.graph)
        self.context.recreate_all()
        self.context.open()

    def teardown(self):
        self.context.close()
        self.graph.postgres.dispose()

    def test_create(self):
        new_user = User(
            username=self.username,
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            title=self.title,
            bio=self.bio,
        )

        with transaction():
            self.user_store.create(new_user)

        retrieved_user = self.user_store.retrieve(new_user.id)
        assert_that(retrieved_user, is_(equal_to(new_user)))

    def test_create_duplicate(self):
        user1 = User(
            username=self.username,
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            title=self.title,
            bio=self.bio,
        )
        user2 = User(
            username=self.username,
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            title=self.title,
            bio=self.bio,
        )

        with transaction():
            self.user_store.create(user1)

        assert_that(
            calling(self.user_store.create).with_args(user2),
            raises(DuplicateModelError),
        )

    def test_retrieve_by_username(self):
        new_user = User(
            username=self.username,
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            title=self.title,
            bio=self.bio,
        )

        with transaction():
            self.user_store.create(new_user)

        retrieved_user = self.user_store.retrieve_by_username(
            self.username
        )

        assert_that(retrieved_user, is_(equal_to(new_user)))
