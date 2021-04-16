from flask import Flask
from .Blueprints import google_auth, comments_api
from sqlalchemy import exc
from datetime import datetime

app = Flask(__name__)
app.config.from_object("config.TestingConfig")

app.register_blueprint(google_auth.blueprint, url_prefix="/login")
app.register_blueprint(comments_api.blueprint)

from .models import db, login_manager, Comment, User
from .utils import youtube_date_format

db.init_app(app)

with app.app_context():
    try:
        db.create_all()
    except exc.OperationalError:
        print("Table already exists!")


login_manager.init_app(app)
# Import routes
from . import views



@app.template_filter('str_slice')
def _jinja2_filter_string_slice(string: str, first, last):
    return string[int(first): int(last)]


@app.template_filter('yt_strftime')
def _jinja2_filter_youtube_datetime(date_time: datetime, fmt=None):
    return youtube_date_format(date_time)
