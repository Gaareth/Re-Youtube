import os
class Config(object):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")

    GOOGLE_OAUTH_CLIENT_ID = os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
    GOOGLE_OAUTH_CLIENT_SECRET = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")

    COMMENT_BATCH_SIZE = 10  # comment to return per request
    MAX_COMMENT_INDENTATION_LEVEL = 3
    COMMENT_MAX_SHOW = 240  # max characters showed in a comment before hidden by collapsable


class ProductionConfig(Config):
    pass


class TestingConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
