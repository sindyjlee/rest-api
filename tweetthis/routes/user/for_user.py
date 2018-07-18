"""
User relation routes.

"""
from microcosm.api import binding
from microcosm_flask.conventions.base import EndpointDefinition
from microcosm_flask.conventions.relation import configure_relation
from microcosm_flask.paging import PageSchema
from microcosm_flask.operations import Operation

from tweetthis.resources.tweet_resources import TweetSchema
from tweetthis.resources.user_resources import UserSchema


@binding("user_relation_routes")
def configure_user_relation_routes(graph):
    configure_search_following_by_user_routes(graph)
    configure_search_followers_by_user_routes(graph)
    configure_search_tweets_by_user_routes(graph)
    configure_search_feed_by_user_routes(graph)


def configure_search_following_by_user_routes(graph):
    """
    Endpoint for list of users the given user is following.

    """
    controller = graph.user_controller

    mappings = {
        Operation.SearchFor: EndpointDefinition(
            func=controller.search_following_by_user,
            request_schema=PageSchema(),
            response_schema=UserSchema(),
        ),
    }

    configure_relation(graph, controller.following_ns, mappings)


def configure_search_followers_by_user_routes(graph):
    """
    Endpoint for list of users following the given user aka followers.

    """
    controller = graph.user_controller

    mappings = {
        Operation.SearchFor: EndpointDefinition(
            func=controller.search_followers_by_user,
            request_schema=PageSchema(),
            response_schema=UserSchema(),
        ),
    }

    configure_relation(graph, controller.followers_ns, mappings)


def configure_search_tweets_by_user_routes(graph):
    """
    Endpoint for list of tweets posted by given user.

    """
    controller = graph.user_controller

    mappings = {
        Operation.SearchFor: EndpointDefinition(
            func=controller.search_tweets_by_user,
            request_schema=PageSchema(),
            response_schema=TweetSchema(),
        ),
    }

    configure_relation(graph, controller.tweets_ns, mappings)


def configure_search_feed_by_user_routes(graph):
    """
    Endpoint for list of tweets posted by users the given user is following.

    """
    controller = graph.user_controller

    mappings = {
        Operation.SearchFor: EndpointDefinition(
            func=controller.search_feed_by_user,
            request_schema=PageSchema(),
            response_schema=TweetSchema(),
        ),
    }

    configure_relation(graph, controller.feed_ns, mappings)
