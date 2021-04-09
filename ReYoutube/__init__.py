from flask import Flask

from .models import db, login_manager
from .Blueprints import google_auth, comment_api

app = Flask(__name__)
app.config.from_object("config.TestingConfig")
app.register_blueprint(google_auth.blueprint, url_prefix="/login")
app.register_blueprint(comment_api.blueprint, url_prefix="/api/comments")

db.init_app(app)
with app.app_context():
    db.create_all()

login_manager.init_app(app)

# Import routes
from . import views
