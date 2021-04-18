from ..models import Notification
from ..models import User, Comment, db


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

        # Only add a notification if the reply is not a self-reply
        # (I don't need a notification for a comment I wrote myself)
        if parent_comment.user != user:
            new_notification = Notification(sender=user,
                                            recipient=parent_comment.user,
                                            link=f"/watch?v={reply.video_id}&auto_collapse#comment-{parent_comment.id}",
                                            content=message)
            db.session.add(new_notification)

        db.session.add(reply)
        db.session.commit()
