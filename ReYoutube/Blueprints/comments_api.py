from flask import Blueprint, request, render_template, jsonify
import werkzeug.exceptions

from flask_login import current_user, login_required
from ..models import User, Comment, db

# comments_upvoted_table, comments_downvoted_table

blueprint = Blueprint('comments_api', __name__, url_prefix="/api/comments")


@blueprint.errorhandler(werkzeug.exceptions.InternalServerError)
def handle_internal_error(e):
    return jsonify({'isError': True, 'status': 500, 'statusText': 'INTERNAL SERVER ERROR'}), 500


@blueprint.errorhandler(werkzeug.exceptions.BadRequest)
def handle_bad_request(e):
    return jsonify({'isError': True, 'status': 400,
                    'statusText': 'Bad Request: '
                                  'The browser (or proxy) sent a request that this server could not understand.'}), 400


@blueprint.route("/upvote_comment", methods=["POST"])
@login_required
def upvote_comment():
    comment_id = request.json["comment_id"]
    comment = Comment.query.filter_by(id=comment_id).first()
    if comment is None:
        return jsonify({'isError': True, 'status': 400,
                        'statusText': 'Bad Request: '
                                      'The browser (or proxy) sent a request that this server could not understand.'}), 400

    current_user.upvote(comment)
    db.session.add_all([comment, current_user])
    db.session.commit()

    return jsonify(has_upvoted=current_user.has_upvoted_comment(comment),
                   has_downvoted=current_user.has_downvoted_comment(comment),
                   upvotes=comment.upvotes,
                   downvotes=comment.downvotes,
                   isError=False, statusCode=200, message="Successfully upvoted Comment")


@blueprint.route("/downvote_comment", methods=["POST"])
@login_required
def downvote_comment():
    comment_id = request.json["comment_id"]
    comment = Comment.query.filter_by(id=comment_id).first()
    if comment is None:
        return jsonify({'isError': True, 'status': 400, 'statusText':
        'Bad Request: The browser (or proxy) sent a request that this server could not understand.'}), 400

    current_user.downvote(comment)
    db.session.add_all([comment, current_user])
    db.session.commit()

    return jsonify(has_upvoted=current_user.has_upvoted_comment(comment),
                   has_downvoted=current_user.has_downvoted_comment(comment),
                   upvotes=comment.upvotes,
                   downvotes=comment.downvotes,
                   isError=False, statusCode=200, message="Successfully downvoted Comment")
