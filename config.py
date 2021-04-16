import os
class Config(object):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")

    GOOGLE_OAUTH_CLIENT_ID = os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
    GOOGLE_OAUTH_CLIENT_SECRET = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")

    PAGE_MAX_COMMENTS = 50  # max comments per page
    MAX_COMMENT_INDENTATION_LEVEL = 3  # how many replies to a comment with a visual indent are allowed
    COMMENT_MAX_SHOW = 240  # max characters showed in a comment before hidden by collapsable
    ALLOWED_HOSTS = ["127.0.0.1:5000"]

class ProductionConfig(Config):
    pass


class DebugConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"


class TestingConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
