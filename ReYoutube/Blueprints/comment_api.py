import math
import urllib.parse as urlparse
from urllib.parse import parse_qs

from flask import redirect, request, jsonify, make_response, Blueprint, current_app
from flask_login import login_required, current_user

from ReYoutube.models import Comment, db

blueprint = Blueprint("comment_api", __name__)


@blueprint.route("/edit", methods=["POST"])
@login_required
def edit_comment():
    pass


@blueprint.route("/delete", methods=["POST"])
@login_required
def delete_comment():
    pass


@blueprint.route("/add", methods=["POST"])
@login_required
def add_comment():
    message = request.form["message"]
    parsed = urlparse.urlparse(request.referrer)
    video_id = parse_qs(parsed.query)['v'][0]
    redirect_link = request.form.get("redirect", False)

    comment = Comment(comment=message, video_id=video_id, user=current_user)

    db.session.add(comment)
    db.session.commit()

    if redirect_link:
        return redirect(f"/watch?v={video_id}")  # url_for with url params??
    return jsonify(isError=False, statusCode=200, message="Successfully added Comment")


@blueprint.route("/load", methods=["POST"])
def load_comments():
    """ Route to return the comments """
    quantity = current_app.config['COMMENT_BATCH_SIZE']
    video_id = request.json["video_id"]
    counter = request.json["counter"]

    num_comments = Comment.query.filter_by(video_id=video_id).count()
    page = math.ceil((counter + 1) / quantity)
    print("Page", page)
    print(num_comments)
    print(counter)

    if counter < num_comments:
        print(f"Returning page {page}")
        comments = Comment.query.filter_by(video_id=video_id).order_by(Comment.created_at.desc()). \
            paginate(page=page, per_page=quantity, error_out=False)

        res = comments.items
        res = (jsonify(list(map(lambda c: c.to_dict(), res))))
    else:
        res = make_response(jsonify({}), 200)

    return res
