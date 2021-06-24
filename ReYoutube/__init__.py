import os

from flask import Flask, session, request, redirect
from .Blueprints import google_auth, api
from sqlalchemy import exc
from datetime import datetime

from .models import db, login_manager, Comment, User
from .utils.time_utils import youtube_date_format

import enum


class AppTheme(enum.Enum):
    DARK = 0
    WHITE = 1


app = Flask(__name__)
app.config.from_object("config.TestingConfig")

app.register_blueprint(google_auth.blueprint, url_prefix="/login")
app.register_blueprint(api.blueprint)

# Initialize Database
db.init_app(app)

with app.app_context():
    try:
        db.create_all()
    except (exc.OperationalError, exc.ProgrammingError):
        print("Table already exists!")

    from .Blueprints import database_cli
    app.register_blueprint(database_cli.blueprint)


login_manager.init_app(app)

# Import routes
from . import views


@app.before_request
def force_https():
    # enfore https by redirecting, except for debugging
    if request.endpoint in app.view_functions and not request.is_secure and not app.config["DEBUG"]:
        return redirect(request.url.replace('http://', 'https://'))


@app.context_processor
def inject_jinja_variables():
    return dict(current_year=datetime.now().year,
                dark_theme=session.get("app_theme", default=AppTheme.WHITE.value) == AppTheme.DARK.value)


@app.template_filter('str_slice')
def _jinja2_filter_string_slice(string: str, first, last):
    return string[int(first): int(last)]


@app.template_filter('yt_strftime')
def _jinja2_filter_youtube_datetime(date_time: datetime, fmt=None):
    return youtube_date_format(date_time)
