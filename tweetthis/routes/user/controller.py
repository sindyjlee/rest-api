"""
User controller.

"""
from microcosm.api import binding
from microcosm_flask.conventions.crud_adapter import CRUDStoreAdapter
from microcosm_flask.namespaces import Namespace

from tweetthis.models.user import User


@binding("user_controller")
class UserController(CRUDStoreAdapter):

    def __init__(self, graph):
        super().__init__(graph, graph.user_store)

        self.ns = Namespace(
            subject=User,
            version="v1",
        )
