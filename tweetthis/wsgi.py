"""
Entrypoint module for WSGI containers.

"""
from tweetthis.app import create_app


app = create_app().app
