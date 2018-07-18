"""
Create the application.

"""
from microcosm.api import create_object_graph
from microcosm.loaders.compose import load_config_and_secrets
from microcosm.loaders import load_each, load_from_environ, load_from_json_file
from microcosm_secretsmanager.loaders.conventions import load_from_secretsmanager

from tweetthis.config import load_default_config
import tweetthis.postgres  # noqa
import tweetthis.routes.follower_relationship.controller  # noqa
import tweetthis.routes.follower_relationship.crud   # noqa
import tweetthis.routes.tweet.controller  # noqa
import tweetthis.routes.tweet.crud   # noqa
import tweetthis.routes.user.controller  # noqa
import tweetthis.routes.user.crud   # noqa
import tweetthis.routes.user.for_user  # noqa
import tweetthis.stores.follower_relationship_store  # noqa
import tweetthis.stores.tweet_store  # noqa
import tweetthis.stores.user_store  # noqa


def create_app(debug=False, testing=False, model_only=False):
    """
    Create the object graph for the application.

    """
    config_loader = load_each(
        load_default_config,
        load_from_environ,
        load_from_json_file,
    )
    partitioned_loader = load_config_and_secrets(
        config=config_loader,
        secrets=load_from_secretsmanager(),
    )

    graph = create_object_graph(
        name=__name__.split(".")[0],
        debug=debug,
        testing=testing,
        loader=partitioned_loader,
    )

    graph.use(
        "follower_relationship_store",
        "tweet_store",
        "user_store",
        "logging",
        "postgres",
        "sessionmaker",
        "session_factory",
    )

    if not model_only:
        graph.use(
            # conventions
            "build_info_convention",
            "config_convention",
            "discovery_convention",
            "health_convention",
            "port_forwarding",
            "postgres_health_check",
            "swagger_convention",
            # routes
            "follower_relationship_routes",
            "tweet_routes",
            "user_routes",
            "user_relation_routes",
        )

    return graph.lock()
