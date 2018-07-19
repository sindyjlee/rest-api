"""
FollowerRelationship Relationship resources.

"""
from marshmallow import fields, Schema

from microcosm_flask.linking import Links, Link
from microcosm_flask.namespaces import Namespace
from microcosm_flask.operations import Operation
from microcosm_flask.paging import PageSchema

from tweetthis.models.follower_relationship import FollowerRelationship
from tweetthis.models.user import User


class NewFollowerRelationshipSchema(Schema):
    userId = fields.UUID(
        required=True,
        attribute="user_id",
    )
    followerId = fields.UUID(
        required=True,
        attribute="follower_id",
    )


class FollowerRelationshipSchema(NewFollowerRelationshipSchema):
    id = fields.UUID(
        required=True,
    )
    createdAt = fields.DateTime(
        required=True,
        attribute="created_at"
    )
    _links = fields.Method(
        "get_links",
        dump_only=True,
    )

    def get_links(self, obj):
        links = Links()
        links["self"] = Link.for_(
            Operation.Retrieve,
            Namespace(
                subject=FollowerRelationship,
                version="v1",
            ),
            follower_relationship_id=obj.id,
        )
        links["user"] = Link.for_(
            Operation.Retrieve,
            Namespace(
                subject=User,
                version="v1",
            ),
            user_id=obj.user_id,
        )
        links["follower"] = Link.for_(
            Operation.Retrieve,
            Namespace(
                subject=User,
                version="v1",
            ),
            user_id=obj.follower_id,
        )
        return links.to_dict()


class SearchFollowerRelationshipSchema(PageSchema):
    user_id = fields.UUID()
    follower_id = fields.UUID()
