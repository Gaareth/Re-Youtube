from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from sqlalchemy.ext.hybrid import hybrid_property

from datetime import datetime

db = SQLAlchemy()


comments_upvoted_table = db.Table('comments_upvoted',
    db.Column('comment_id', db.Integer, db.ForeignKey('comment.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

comments_downvoted_table = db.Table('comments_downvoted',
    db.Column('comment_id', db.Integer, db.ForeignKey('comment.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    sender_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    content = db.Column(db.String)

    def __repr__(self):
        return f"<Notification {self.sender_id} -> {self.recipient_id}>"


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    profile_picture = db.Column(db.String)

    comments = db.relationship("Comment", backref="user")

    comments_upvoted = db.relationship('Comment', secondary=comments_upvoted_table, lazy='subquery',
        backref=db.backref('users_upvoted', lazy=True))
    comments_downvoted = db.relationship('Comment', secondary=comments_downvoted_table, lazy='subquery',
        backref=db.backref('users_downvoted', lazy=True))

    '''comments_upvoted = db.relationship('Comment', backref=db.backref('users_upvoted', lazy=True))
    comments_downvoted = db.relationship('Comment', backref=db.backref('users_downvoted', lazy=True))'''

    notifications_send = db.relationship(
        "Notification", foreign_keys="Notification.sender_id", backref="sender"
    )
    notifications_received = db.relationship(
        "Notification", foreign_keys="Notification.recipient_id", backref="recipient"
    )

    notifications_last_checked = db.Column(db.DateTime)

    def __repr__(self):
        return '<User %r>' % self.username

    def new_notifications(self):
        last_read_time = self.notifications_last_checked or datetime(1900, 1, 1)
        return Notification.query.filter_by(recipient=self).filter(
            Notification.timestamp > last_read_time).count()

    def upvote(self, comment):
        if comment not in self.comments_upvoted:

            if comment in self.comments_downvoted:
                self.comments_downvoted.remove(comment)
                comment.downvotes -= 1

            self.comments_upvoted.append(comment)
            comment.upvotes += 1
        else:
            self.comments_upvoted.remove(comment)
            comment.upvotes -= 1

    def downvote(self, comment):
        if comment not in self.comments_downvoted:

            if comment in self.comments_upvoted:
                self.comments_upvoted.remove(comment)
                comment.upvotes -= 1

            self.comments_downvoted.append(comment)
            comment.downvotes += 1
        else:
            self.comments_downvoted.remove(comment)
            comment.downvotes -= 1

    def has_upvoted_comment(self, comment):
        return comment in self.comments_upvoted

    def has_downvoted_comment(self, comment):
        return comment in self.comments_downvoted


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    comment = db.Column(db.String, nullable=False)

    is_edited = db.Column(db.Boolean, default=False)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    replies = db.relationship(
        'Comment', backref=db.backref('parent', remote_side=[id]),
        lazy='dynamic')

    upvotes = db.Column(db.Integer, default=0)
    downvotes = db.Column(db.Integer, default=0)

    @hybrid_property
    def rating(self):
        return self.upvotes - self.downvotes

    def add_reply(self, text: str, user: User):
        return Comment(comment=text, parent=self, video_id=self.video_id, user=user)

    def __repr__(self):
        return f"Comment [{self.video_id}] ({self.user}) [Up: {self.upvotes}, Down: {self.downvotes}]"


class OAuth(OAuthConsumerMixin, db.Model):
    provider_user_id = db.Column(db.String(256), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    user = db.relationship(User)


# setup login manager
login_manager = LoginManager()
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
