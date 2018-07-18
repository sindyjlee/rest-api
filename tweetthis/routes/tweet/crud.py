"""
Tweet CRUD routes.

"""
from microcosm.api import binding
from microcosm_flask.conventions.base import EndpointDefinition
from microcosm_flask.conventions.crud import configure_crud
from microcosm_flask.operations import Operation
from microcosm_postgres.context import transactional

from tweetthis.resources.tweet_resources import (
    NewTweetSchema,
    SearchTweetSchema,
    TweetSchema,
)


@binding("tweet_routes")
def configure_tweet_routes(graph):
    controller = graph.tweet_controller
    mappings = {
        Operation.Create: EndpointDefinition(
            func=transactional(controller.create),
            request_schema=NewTweetSchema(),
            response_schema=TweetSchema(),
        ),
        Operation.Delete: EndpointDefinition(
            func=transactional(controller.delete),
        ),
        Operation.Retrieve: EndpointDefinition(
            func=controller.retrieve,
            response_schema=TweetSchema(),
        ),
        Operation.Search: EndpointDefinition(
            func=controller.search,
            request_schema=SearchTweetSchema(),
            response_schema=TweetSchema(),
        ),
    }
    configure_crud(graph, controller.ns, mappings)
    return controller.ns
