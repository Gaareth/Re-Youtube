from datetime import datetime, timedelta
from .models import Comment, User, db


def edit_comment(comment_id: int, new_message: str):
    """ Function to edit a comment """
    old_comment = Comment.query.filter_by(id=comment_id).first()
    old_comment.comment = new_message
    old_comment.is_edited = True
    db.session.commit()


def delete_comment(comment_id):
    """ Function to delete a comment from the database """
    db.session.delete(Comment.query.filter_by(id=comment_id).first())
    db.session.commit()


def add_comment(message: str, video_id: str, user: User):
    """ Function to add a new comment to the database """
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
    parent_comment = Comment.query.filter_by(id=parent_comment_id).first()
    reply = parent_comment.add_reply(message, user)
    db.session.add(reply)
    db.session.commit()


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
