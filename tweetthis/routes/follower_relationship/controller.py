"""
Follower Relationship controller.

"""
from microcosm.api import binding
from microcosm_flask.conventions.crud_adapter import CRUDStoreAdapter
from microcosm_flask.namespaces import Namespace

from tweetthis.models.follower_relationship import FollowerRelationship


@binding("follower_relationship_controller")
class FollowerRelationshipController(CRUDStoreAdapter):

    def __init__(self, graph):
        super().__init__(graph, graph.follower_relationship_store)

        self.ns = Namespace(
            subject=FollowerRelationship,
            version="v1",
        )
