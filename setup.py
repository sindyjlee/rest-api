#!/usr/bin/env python
from setuptools import find_packages, setup

project = "tweetthis"
version = "0.1.0"

setup(
    name=project,
    version=version,
    description="RESTful service",
    author="Sindy J. Lee",
    author_email="code@sindylee.com",
    url="https://github.com/sindyjlee/rest-api",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "microcosm>=2.4.0",
        "microcosm-secretsmanager>=1.1.0",
        "microcosm-flask[metrics,spooky]>=1.5.1",
        "microcosm-logging>=1.0.0",
        "microcosm-postgres>=1.1.0",
        "pyOpenSSL>=17.5.0",
        # until botocore stops enforcing: python-dateutil>=2.1,<2.7.0
        # "python-dateutil==2.6.1",
        "python-dateutil>=2.7.3",
    ],
    setup_requires=[
        "nose>=1.3.7",
    ],
    entry_points={
        "console_scripts": [
            "createall = tweetthis.main:createall",
            "migrate = tweetthis.main:migrate",
            "runserver = tweetthis.main:runserver",
        ],
    },
    tests_require=[
        "coverage>=4.0.3",
        "mock>=2.0.0",
        "PyHamcrest>=1.9.0",
    ],
)
