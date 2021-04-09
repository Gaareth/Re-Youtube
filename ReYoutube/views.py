from ReYoutube import app
from flask import render_template
from flask_login import login_required, logout_user, current_user
from flask import Flask, redirect, url_for, flash, render_template, request, jsonify, make_response
from .models import User, Comment, db


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have logged out")
    return redirect(url_for("index"))



@app.route("/")
def index():
    return render_template("index.html")


@app.route("/watch")
def watch():
    if video_id := request.args.get("v"):
        num_comments = Comment.query.filter_by(video_id=video_id).count()
        return render_template("watch.html", video_id=video_id, num_comments=num_comments)
    else:
        return redirect(url_for("index"))
