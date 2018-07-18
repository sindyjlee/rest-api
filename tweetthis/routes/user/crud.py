"""
User CRUD routes.

"""
from microcosm.api import binding
from microcosm_flask.conventions.base import EndpointDefinition
from microcosm_flask.conventions.crud import configure_crud
from microcosm_flask.operations import Operation
from microcosm_postgres.context import transactional

from tweetthis.resources.user_resources import (
    NewUserSchema,
    SearchUserSchema,
    UpdateUserSchema,
    UserSchema,
)


@binding("user_routes")
def configure_user_routes(graph):
    controller = graph.user_controller
    mappings = {
        Operation.Create: EndpointDefinition(
            func=transactional(controller.create),
            request_schema=NewUserSchema(),
            response_schema=UserSchema(),
        ),
        Operation.Delete: EndpointDefinition(
            func=transactional(controller.delete),
        ),
        Operation.Retrieve: EndpointDefinition(
            func=controller.retrieve,
            response_schema=UserSchema(),
        ),
        Operation.Search: EndpointDefinition(
            func=controller.search,
            request_schema=SearchUserSchema(),
            response_schema=UserSchema(),
        ),
        Operation.Update: EndpointDefinition(
            func=transactional(controller.update),
            request_schema=UpdateUserSchema(),
            response_schema=UserSchema(),
        ),
    }
    configure_crud(graph, controller.ns, mappings)
    return controller.ns
