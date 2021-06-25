# -*- coding: utf-8 -*-
"""service configuration module
"""
import os

# api settings
DEBUG = os.environ.get("DEBUG", False)
ERROR_INCLUDE_MESSAGE = False


# database settings
DB_CONNECTION_TYPE = os.environ.get("DB_CONNECTION_TYPE")
DB_HOST = os.environ.get("DB_HOST")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")
SQLALCHEMY_DATABASE_URI = os.environ.get(
    "SQLALCHEMY_DATABASE_URI",
    f"{DB_CONNECTION_TYPE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}",
)

# GCP PUBSUB
GCP_PUBSUB_TOPIC = os.environ.get("GCP_PUBSUB_TOPIC")
GCP_PUBSUB_PROJECT = os.environ.get("GCP_PUBSUB_PROJECT")
GCP_PUBSUB_SUB = os.environ.get("GCP_PUBSUB_SUB")
