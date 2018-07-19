"""
Tweet resources.

"""
from marshmallow import fields, Schema

from microcosm_flask.linking import Links, Link
from microcosm_flask.namespaces import Namespace
from microcosm_flask.operations import Operation
from microcosm_flask.paging import PageSchema

from tweetthis.models.tweet import Tweet
from tweetthis.models.user import User


class NewTweetSchema(Schema):
    userId = fields.UUID(
        required=True,
        attribute="user_id",
    )
    tweetContent = fields.String(
        required=True,
        attribute="tweet_content",
    )


class TweetSchema(NewTweetSchema):
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
                subject=Tweet,
                version="v1",
            ),
            tweet_id=obj.id,
        )
        links["user"] = Link.for_(
            Operation.Retrieve,
            Namespace(
                subject=User,
                version="v1",
            ),
            user_id=obj.user_id,
        )
        return links.to_dict()


class SearchTweetSchema(PageSchema):
    user_id = fields.UUID()
    tweet_content_substring = fields.String()
