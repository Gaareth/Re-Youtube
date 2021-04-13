from ReYoutube import app
from flask import render_template
from flask_login import login_required, logout_user, current_user, user_logged_in
from flask import Flask, redirect, url_for, flash, render_template, request, jsonify, make_response

from . import utils
from .models import User, Comment, db


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have logged out", "primary")
    return redirect(url_for("index"))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/watch", methods=["GET", "POST"])
@app.route("/watch/page/<int:page>", methods=["GET", "POST"])
def watch(page=1):
    if request.method == "POST":
        action = request.form["action"]
        video_id = request.form["video_id"]
        print("Action", action)
        if current_user.is_authenticated:
            comment_message = request.form.get("message")
            comment_id = request.form.get("comment_id")

            comment_parent = None
            open_all_replies = ""
            if comment_id is not None:
                comment_parent = Comment.query.filter_by(id=comment_id).first().parent
                open_all_replies = "&auto_collapse=False"

            url_params = f"{open_all_replies if action == 'reply' or comment_parent is not None else ''}" \
                         f"#comment-{comment_id}"

            if action == "add":
                utils.add_comment(comment_message, video_id, current_user)
            elif action == "edit":
                utils.edit_comment(comment_id, comment_message)
            elif action == "delete":
                utils.delete_comment(comment_id)
            elif action == "reply":
                utils.add_reply(comment_message, current_user, comment_id)

            # Scroll to the interacted comment or redirect to the correct page
            return redirect(f"{url_for('watch', page=page)}?v={video_id}{url_params if comment_id is not None else ''}")
        else:
            flash("Please login first", "danger")
        return redirect(f"{url_for('watch', page=page)}?v={video_id}")

    if video_id := request.args.get("v"):
        comment_query = Comment.query.filter_by(video_id="1xIaoqxiZRA")
        num_comments = comment_query.count()
        comments = comment_query.filter_by(parent=None).order_by(Comment.created_at.desc()).\
            paginate(page=page, per_page=app.config['COMMENT_BATCH_SIZE'], error_out=False)
        return render_template("watch.html", comments=comments, auto_collapse=request.args.get("auto_collapse"),
                               video_id=video_id, num_comments=num_comments)
    else:
        return redirect(url_for("index"))
