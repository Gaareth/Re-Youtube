from flask import redirect, url_for, flash, render_template, request, session
from flask_login import login_required, logout_user, current_user
from is_safe_url import is_safe_url

from ReYoutube import app, AppTheme
from . import utils
from .models import Comment


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have logged out", "primary")
    next_url = request.referrer
    if not is_safe_url(next_url, allowed_hosts=app.config["ALLOWED_HOSTS"]):
        next_url = url_for("index")
    return redirect(next_url)


@app.route("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # Redirect to referrer url after login
    session['next_url'] = request.referrer
    return redirect(url_for("google.login"))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/tos")
def tos():
    return render_template("tos.html")


@app.route("/privacy_policy")
def privacy_policy():
    return render_template("privacyPolicy.html")


@app.route("/set_theme", methods=["POST"])
def set_app_theme():
    # toggle app theme
    current_theme = session.get("app_theme")

    if current_theme == AppTheme.WHITE.value or current_theme is None:
        session["app_theme"] = AppTheme.DARK.value
    else:
        session["app_theme"] = AppTheme.WHITE.value

    # redirect to referrer (if safe)
    next_url = request.referrer if is_safe_url(request.referrer, allowed_hosts=app.config["ALLOWED_HOSTS"]) else "/"
    return redirect(next_url)


@app.route("/watch", methods=["GET", "POST"])
@app.route("/watch/page/<int:page>", methods=["GET", "POST"])
def watch(page=1):
    if request.method == "POST":
        return utils.process_post_action(request, page)

    if video_id := request.args.get("v"):
        comment_query = Comment.query.filter_by(video_id=video_id)
        num_comments = comment_query.count()
        # Choose the order contrary to the current used one
        # In order to change the order from Asc to Desc.
        current_sort_order = request.args.get("o", "asc")
        sort_options = {
            "upload_date": Comment.created_at.desc() if current_sort_order == "asc" else Comment.created_at.asc(),
            "rating": Comment.rating.desc() if current_sort_order == "asc" else Comment.rating.asc()
        }
        sort_by = request.args.get("s", "upload_date")

        comments = comment_query.filter_by(parent=None). \
            order_by(sort_options.get(sort_by)). \
            paginate(page=page, per_page=app.config['PAGE_MAX_COMMENTS'], error_out=False)

        return render_template("watch.html",
                               comments=comments, auto_collapse=request.args.get("auto_collapse"),
                               video_id=video_id, num_comments=num_comments,
                               current_order=f"{'asc' if current_sort_order == 'desc' else 'desc'}",
                               current_sorting=sort_by)
    else:
        return redirect(url_for("index"))
