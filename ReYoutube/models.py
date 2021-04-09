from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin

from datetime import datetime
from ReYoutube.utils import youtube_date_format

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    # email = db.Column(db.String, unique=True, nullable=False)
    profile_picture = db.Column(db.String)

    comments = db.relationship("Comment", backref="user")

    def __repr__(self):
        return '<User %r>' % self.username

    # note: comments is missing
    def to_dict(self):
        return {"id": self.id, "username": self.username, "profile_picture": self.profile_picture}


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.now())
    comment = db.Column(db.String, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"Comment [{self.video_id}] ({self.user}): {self.comment} "

    # for the lazy data loading
    def to_dict(self):
        return {"id": self.id,
                "video_id": self.video_id,
                "created_at": [self.created_at, youtube_date_format(self.created_at)],
                "comment": self.comment,
                "user_id": self.user_id,
                "user": self.user.to_dict()}


class OAuth(OAuthConsumerMixin, db.Model):
    provider_user_id = db.Column(db.String(256), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    user = db.relationship(User)


# setup login manager
login_manager = LoginManager()
login_manager.login_view = "google.login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
