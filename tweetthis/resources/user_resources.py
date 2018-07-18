"""
User resources.

"""
from marshmallow import fields, Schema

from microcosm_flask.linking import Links, Link
from microcosm_flask.namespaces import Namespace
from microcosm_flask.operations import Operation
from microcosm_flask.paging import PageSchema

from tweetthis.models.user import User


class NewUserSchema(Schema):
    username = fields.String(
        required=True,
    )
    email = fields.Email(
        required=True,
    )
    firstName = fields.String(
        attribute="first_name",
        required=True,
    )
    lastName = fields.String(
        attribute="last_name",
        required=True,
    )
    title = fields.String(
        allow_none=True,
    )
    bio = fields.String(
        allow_none=True,
    )


class UpdateUserSchema(Schema):
    id = fields.UUID(
        required=True,
    )
    firstName = fields.String(
        attribute="first_name",
        required=True,
    )
    lastName = fields.String(
        attribute="last_name",
        required=True,
    )
    title = fields.String(
        allow_none=True,
    )
    bio = fields.String(
        allow_none=True,
    )


class UserSchema(NewUserSchema):
    id = fields.UUID(
        required=True,
    )
    createdAt = fields.DateTime(
        required=True,
        attribute="created_at"
    )
    updatedAt = fields.DateTime(
        required=True,
        attribute="updated_at"
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
                subject=User,
                version="v1",
            ),
            user_id=obj.id,
        )
        return links.to_dict()


class SearchUserSchema(PageSchema):
    username = fields.String()
    email = fields.Email()
    first_name = fields.String()
    last_name = fields.String()
