"""
Tweet controller.

"""
from microcosm.api import binding
from microcosm_flask.conventions.crud_adapter import CRUDStoreAdapter
from microcosm_flask.namespaces import Namespace

from tweetthis.models.tweet import Tweet


@binding("tweet_controller")
class TweetController(CRUDStoreAdapter):

    def __init__(self, graph):
        super().__init__(graph, graph.tweet_store)

        self.ns = Namespace(
            subject=Tweet,
            version="v1",
        )
