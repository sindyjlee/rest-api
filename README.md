# REST API: `tweetthis`

Example RESTful service to support a simple Twitter-like webapp.

Built using Python 3.6.5 with [Flask](http://flask.pocoo.org/), [SQLAlchemy](https://www.sqlalchemy.org/), and [PostgreSQL](https://www.postgresql.org/) using open-source microcosm libraries at https://code.globality.com to facilitate microservice setup.


## Setup

To setup the project in your local environment, make sure you have a `virtualenv` setup, and then run:

    pip3 install -e .

This will install all the dependencies and set the project up for local usage.

### PostgreSQL

The service requires a PostgreSQL user and two databases (one is for testing).  After making sure PostgreSQL is installed and running, run the following:

    createuser tweetthis
    createdb -O tweetthis tweetthis_db
    createdb -O tweetthis tweetthis_test_db

Once created, the service schema can be initialized using (use `-D` to drop all existing tables):

    createall [-D]

### Running Tests

To run tests, run:

    pip3 install mock nose pyhamcrest coverage

This will install dependencies for running tests.  Then run:

    nosetests

This will run unit tests as well as print out test coverage.


## Run Service via Flask

To run the Flask web server locally, invoke the following:

    runserver

Refer to the output for details; the service will be available at http://127.0.0.1:5000/.

The service publishes several endpoints by default.

 -  The service publishes its own health:

        GET /api/health

 -  The service publishes a [crawlable](https://en.wikipedia.org/wiki/HATEOAS) endpoint for discovery
    of its operations:

        GET /api/

 -  The service publishes [Swagger](http://swagger.io/) definitions for its operations (by API version)
    using [HAL JSON](http://stateless.co/hal_specification.html):

        GET /api/v1/swagger
