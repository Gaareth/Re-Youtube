from flask import Blueprint, request, render_template, jsonify
import werkzeug.exceptions
from functools import wraps
from flask_login import current_user, login_required
from ..models import User, Comment, db

from ..utils import comment_utils

blueprint = Blueprint('comments_api', __name__, url_prefix="/api")


def is_authenticated_api(func):
    """return jsonified error in case user is not authenticated to access endpoint"""

    @wraps(func)
    def wrap(*args, **kwargs):
        if current_user.is_authenticated:
            return func(*args, **kwargs)
        else:
            return jsonify(isError=True, status=401, statusText="Unauthorized. Please log in first."), 401

    return wrap


# GET
@blueprint.route("/is_authenticated")
def is_authenticated():
    return jsonify(is_authenticated=current_user.is_authenticated)


@blueprint.route("/users/self/get_user")
@is_authenticated_api
def get_user_self():
    return current_user.serialize()


@blueprint.route("/users/get_user/<int:user_id>")
def get_user_by_id(user_id):
    user = User.query.get(user_id)
    if user is not None:
        return user.serialize()
    else:
        return jsonify(isError=True, status=404, statusText="User not found"), 404


@blueprint.route("/users/self/get_notifications")
@is_authenticated_api
def get_notifications():
    return jsonify([notify.serialize() for notify in current_user.get_notifications()])


@blueprint.route("/comments/self/get_comment_vote_status/<int:comment_id>")
@is_authenticated_api
def get_comment_vote_status(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment is not None:
        return jsonify(
            upvoted=current_user.has_upvoted_comment(comment),
            downvoted=current_user.has_downvoted_comment(comment)
        )
    else:
        return jsonify(isError=True, status=404, statusText="Comment not found"), 404


@blueprint.route("/comments/get_comments/<video_id>")
def get_comments_by_video_id(video_id):
    comments = Comment.query.filter_by(video_id=video_id)
    if comments is not None:
        return jsonify([comment.serialize() for comment in comments])
    else:
        return jsonify(isError=True, status=404, statusText="Video not found"), 404


# POSTS
@blueprint.route("/comments/self/upvote_comment", methods=["POST"])
@is_authenticated_api
def upvote_comment():
    comment_id = request.json["comment_id"]
    comment = Comment.query.get(comment_id)
    if comment is None:
        return jsonify(isError=True, status=404, statusText="Comment not found"), 404

    current_user.upvote(comment)
    db.session.add_all([comment, current_user])
    db.session.commit()

    return jsonify(has_upvoted=current_user.has_upvoted_comment(comment),
                   has_downvoted=current_user.has_downvoted_comment(comment),
                   upvotes=comment.upvotes,
                   downvotes=comment.downvotes,
                   isError=False, statusCode=200, message="Successfully upvoted Comment")


@blueprint.route("/comments/self/downvote_comment", methods=["POST"])
@is_authenticated_api
def downvote_comment():
    comment_id = request.json["comment_id"]
    comment = Comment.query.filter_by(id=comment_id).first()
    if comment is None:
        return jsonify(isError=True, status=404, statusText="Comment not found"), 404

    current_user.downvote(comment)
    db.session.add_all([comment, current_user])
    db.session.commit()

    return jsonify(has_upvoted=current_user.has_upvoted_comment(comment),
                   has_downvoted=current_user.has_downvoted_comment(comment),
                   upvotes=comment.upvotes,
                   downvotes=comment.downvotes,
                   isError=False, statusCode=200, message="Successfully downvoted Comment")


# Comments
@blueprint.route("/comments/self/add_comment", methods=["POST"])
@is_authenticated_api
def add_comment():
    """ Add a comment to a video

        Post Arguments:
            video_id= The Youtube video id\n
            comment_content= Content/Message of the comment

    """
    try:
        video_id = request.json["video_id"]
        comment_content = request.json["comment_content"]

        response_code = comment_utils.add_comment(message=comment_content, video_id=video_id, user=current_user)
        return jsonify(statusCode=response_code), response_code
    except (KeyError, TypeError) as e:
        return handle_bad_request(e)


@blueprint.route("/comments/self/add_reply", methods=["POST"])
@is_authenticated_api
def add_reply():
    """ Add a reply to a parent comment

        Post Arguments:
            parent_id= ID of the parent comment
            comment_content= Content/Message of the reply

    """
    try:
        parent_id = request.json["parent_id"]
        comment_content = request.json["comment_content"]

        response_code = comment_utils.add_reply(message=comment_content, parent_comment_id=parent_id, user=current_user)
        return jsonify(statusCode=response_code), response_code
    except (KeyError, TypeError) as e:
        return handle_bad_request(e)


@blueprint.route("/comments/self/edit_comment", methods=["POST"])
@is_authenticated_api
def edit_comment():
    """ Edit comment

        Post Arguments:
            comment_id= ID of the comment that should be edited
            comment_content= New content of the comment

    """
    try:
        comment_id = request.json["comment_id"]
        comment_content = request.json["comment_content"]

        response_code = comment_utils.edit_comment(comment_id, comment_content)
        return jsonify(statusCode=response_code), response_code
    except (KeyError, TypeError) as e:
        return handle_bad_request(e)


@blueprint.route("/comments/self/delete_comment", methods=["POST"])
@is_authenticated_api
def delete_comment():
    """ Delete comment

        Post Arguments:
            comment_id= ID of the comment that should be deleted

    """
    try:
        comment_id = request.json["comment_id"]
        response_code = comment_utils.delete_comment(comment_id)
        return jsonify(statusCode=response_code), response_code
    except (KeyError, TypeError) as e:
        return handle_bad_request(e)


# errors
@blueprint.errorhandler(werkzeug.exceptions.InternalServerError)
def handle_internal_error(e):
    return jsonify({'isError': True, 'status': 500, 'statusText': 'INTERNAL SERVER ERROR'}), 500


@blueprint.errorhandler(werkzeug.exceptions.BadRequest)
def handle_bad_request(e):
    return jsonify({'isError': True, 'status': 400,
                    'statusText': 'Bad Request: '
                                  'The browser (or proxy) sent a request that this server could not understand.'}), 400
