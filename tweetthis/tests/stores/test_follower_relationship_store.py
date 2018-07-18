"""
Follower Relationship persistence tests.

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
from tweetthis.models.follower_relationship import FollowerRelationship
from tweetthis.models.user import User


class TestFollowerRelationship:

    def setup(self):
        self.graph = create_app(testing=True)
        self.user_store = self.graph.user_store
        self.follower_relationship_store = self.graph.follower_relationship_store

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

        self.context = SessionContext(self.graph)
        self.context.recreate_all()
        self.context.open()

        with transaction():
            self.user1.create()
            self.user2.create()

    def teardown(self):
        self.context.close()
        self.graph.postgres.dispose()

    def test_create(self):
        new_follower_relationship = FollowerRelationship(
            user_id=self.user1.id,
            follower_id=self.user2.id,
        )

        with transaction():
            self.follower_relationship_store.create(new_follower_relationship)

        retrieved_follower_relationship = self.follower_relationship_store.retrieve(new_follower_relationship.id)
        assert_that(retrieved_follower_relationship, is_(equal_to(new_follower_relationship)))

    def test_create_duplicate(self):
        follower_relationship1 = FollowerRelationship(
            user_id=self.user1.id,
            follower_id=self.user2.id,
        )
        follower_relationship2 = FollowerRelationship(
            user_id=self.user1.id,
            follower_id=self.user2.id,
        )

        with transaction():
            self.follower_relationship_store.create(follower_relationship1)

        assert_that(
            calling(self.follower_relationship_store.create).with_args(follower_relationship2),
            raises(DuplicateModelError),
        )
