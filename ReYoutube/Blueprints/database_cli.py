import os
import sys
from flask import Blueprint
from ReYoutube import db, app
from ReYoutube.models import \
    User, Comment, Notification, comments_upvoted_table, comments_downvoted_table, OAuth

blueprint = Blueprint('database', __name__)


#  https://stackoverflow.com/a/1094933
def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


@blueprint.cli.command('size')
def get_size():
    # I don't know how reliable this is
    db_name = app.config["SQLALCHEMY_DATABASE_URI"].split("sqlite:///")[1]
    db_size = os.path.getsize(f'{sys.path[0]}/ReYoutube/{db_name}')
    print(sizeof_fmt(db_size))


@blueprint.cli.command('rows')
def get_rows():
    """ Returns num of rows """
    # Please tell me there is a better way
    rows_user = db.session.query(User).count()
    rows_comment = db.session.query(Comment).count()
    rows_notification = db.session.query(Notification).count()
    rows_upv = db.session.query(comments_upvoted_table).count()
    rows_downv = db.session.query(comments_downvoted_table).count()
    rows_auth = rows_user

    total_rows = rows_user + rows_comment + rows_notification + rows_upv + rows_downv + rows_auth
    print(f"Total rows: {total_rows}")
