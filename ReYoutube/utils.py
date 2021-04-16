from datetime import datetime, timedelta

from flask import redirect, url_for, flash, render_template
from flask_login import current_user

from . import app
from .models import Notification
from .models import User, Comment, db

import urllib


def edit_comment(comment_id: int, new_message: str):
    """ Function to edit a comment """
    if len(new_message) > 0:
        old_comment = Comment.query.filter_by(id=comment_id).first()
        if old_comment is None:
            return
        old_comment.comment = new_message
        old_comment.is_edited = True
        db.session.commit()


def delete_comment(comment_id):
    """ Function to delete a comment from the database """
    comment_to_delete = Comment.query.filter_by(id=comment_id).first()
    if comment_to_delete is not None:
        db.session.delete(comment_to_delete)
        db.session.commit()


def add_comment(message: str, video_id: str, user: User):
    """ Function to add a new comment to the database """
    if len(message) > 0:
        comment = Comment(comment=message, video_id=video_id, user=user)
        db.session.add(comment)
        db.session.commit()


def add_reply(message: str, user: User, parent_comment_id: int):
    """ Function to add a reply to another comment

        Args:
            message: The text of the reply
            user: current User object
            parent_comment_id: ID of the comment that should be replied to
    """
    if len(message) > 0:
        parent_comment = Comment.query.filter_by(id=parent_comment_id).first()
        if parent_comment is None:
            return

        reply = parent_comment.add_reply(message, user)
        new_notification = Notification(sender=user, recipient=parent_comment.user)
        db.session.add_all([reply, new_notification])
        db.session.commit()

def process_post_action(request, page):
    action = request.form["action"]
    video_id = request.form["video_id"]
    print("Action", action)
    if current_user.is_authenticated:
        comment_message = request.form.get("message")
        comment_id = request.form.get("comment_id")

        url_arg_dict = {"v": video_id}

        if comment_id is not None:
            if comment := Comment.query.filter_by(id=comment_id).first():
                if comment.parent is not None:
                    url_arg_dict['auto_collapse'] = False

        if action == "add":
            add_comment(comment_message, video_id, current_user)
        elif action == "edit":
            edit_comment(comment_id, comment_message)
        elif action == "delete":
            delete_comment(comment_id)
        elif action == "reply":
            add_reply(comment_message, current_user, comment_id)
        elif action == "sort":
            sort_by = request.form.get("sort_by")
            order = request.form.get("sort_order")

            url_arg_dict["s"] = sort_by
            url_arg_dict["o"] = order

        url_params = urllib.parse.urlencode(url_arg_dict)


        # Scroll to the interacted comment or redirect to the correct page
        return redirect(f"{url_for('watch', page=page)}?{url_params}{f'#comment-{comment_id}' if comment_id else ''}")
    else:
        flash("Please login first", "danger")
    return redirect(f"{url_for('watch', page=page)}?v={video_id}")



# TODO: please rewrite
def youtube_date_format(date_input: datetime) -> str:
    diff = datetime.now() - date_input

    if diff <= timedelta(seconds=1):
        return "Now"
    elif diff <= timedelta(minutes=1):
        date = diff.seconds
        mode = "seconds" if date > 1 else "second"
    elif diff <= timedelta(hours=1):
        date = diff.seconds // 60
        mode = "minutes" if date > 1 else "minute"
    elif diff <= timedelta(hours=24):
        date = diff.seconds // 60 // 60
        mode = "hours" if date > 1 else "hour"
    elif diff <= timedelta(days=30):
        date = diff.seconds // 60 // 60 // 24
        mode = "days" if date > 1 else "day"
    elif diff <= timedelta(days=30 * 12):
        date = diff.seconds // 60 // 60 // 24 // 30
        mode = "months" if date > 1 else "month"
    else:
        date = diff.seconds // 60 // 60 // 24 // 30 // 12
        mode = "years" if date > 1 else "year"

    # print(f"{date} {mode} ago")
    # print(diff)
    return f"{date} {mode} ago"
