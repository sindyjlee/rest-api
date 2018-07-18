"""
Follower Relationship CRUD routes.

"""
from microcosm.api import binding
from microcosm_flask.conventions.base import EndpointDefinition
from microcosm_flask.conventions.crud import configure_crud
from microcosm_flask.operations import Operation
from microcosm_postgres.context import transactional

from tweetthis.resources.follower_relationship_resources import (
    NewFollowerRelationshipSchema,
    SearchFollowerRelationshipSchema,
    FollowerRelationshipSchema,
)


@binding("follower_relationship_routes")
def configure_follower_relationship_routes(graph):
    controller = graph.follower_relationship_controller
    mappings = {
        Operation.Create: EndpointDefinition(
            func=transactional(controller.create),
            request_schema=NewFollowerRelationshipSchema(),
            response_schema=FollowerRelationshipSchema(),
        ),
        Operation.Delete: EndpointDefinition(
            func=transactional(controller.delete),
        ),
        Operation.Retrieve: EndpointDefinition(
            func=controller.retrieve,
            response_schema=FollowerRelationshipSchema(),
        ),
        Operation.Search: EndpointDefinition(
            func=controller.search,
            request_schema=SearchFollowerRelationshipSchema(),
            response_schema=FollowerRelationshipSchema(),
        ),
    }
    configure_crud(graph, controller.ns, mappings)
    return controller.ns
