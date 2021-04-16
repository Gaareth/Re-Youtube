from flask import flash, session, redirect, abort, current_app
from is_safe_url import is_safe_url

from flask_login import current_user, login_user
from flask_dance.contrib.google import make_google_blueprint
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from sqlalchemy.orm.exc import NoResultFound
from ReYoutube.models import db, User, OAuth

blueprint = make_google_blueprint(
    scope=["profile", "https://www.googleapis.com/auth/youtube.readonly"],
    storage=SQLAlchemyStorage(OAuth, db.session, user=current_user),
)



# create/login local user on successful OAuth login
@oauth_authorized.connect_via(blueprint)
def google_logged_in(blueprint, token):
    if not token:
        flash("Failed to log in.", category="danger")
        return redirect_next()

    resp = blueprint.session.get("/oauth2/v1/userinfo")
    # Get Youtube Channel Info
    resp_yt = blueprint.session.get("https://youtube.googleapis.com/youtube/v3/channels?part=snippet&mine=true")

    if not resp.ok or not resp_yt.ok:
        msg = "Failed to fetch user info."
        flash(msg, category="danger")
        return redirect_next()

    user_id = resp.json()["id"]

    info_yt = resp_yt.json()
    if "items" not in info_yt:
        #TODO: implement google account usage
        flash("Please choose an actual Youtube Account!", "danger")
        return redirect_next()

    user_name = info_yt["items"][0]["snippet"]["title"]
    thumbnail = info_yt["items"][0]["snippet"]["thumbnails"]["default"]["url"]

    # Find this OAuth token in the database, or create it
    query = OAuth.query.filter_by(provider=blueprint.name, provider_user_id=user_id)
    try:
        oauth = query.one()
    except NoResultFound:
        oauth = OAuth(provider=blueprint.name, provider_user_id=user_id, token=token)

    if oauth.user:
        login_user(oauth.user)
        flash("Successfully signed in.", "success")
        return redirect_next()
    else:
        # Create a new local user account for this user
        user = User(username=user_name, profile_picture=thumbnail)
        # Associate the new local user account with the OAuth token
        oauth.user = user
        # Save and commit our database models
        db.session.add_all([user, oauth])
        db.session.commit()
        # Log in the new local user account
        login_user(user)
        flash("Successfully signed in.", "success")

        return redirect_next()

def redirect_next():
    from .. import app

    # get next_url , default is index
    next_url = session.get("next_url", "/")
    print(next_url)
    if not is_safe_url(next_url, allowed_hosts=app.config["ALLOWED_HOSTS"]):
        return abort(400)
    # redirect the user to `next_url`
    return redirect(next_url)

# notify on OAuth provider error
@oauth_error.connect_via(blueprint)
def google_error(blueprint, message, response):
    msg = ("OAuth error from {name}! " "message={message} response={response}").format(
        name=blueprint.name, message=message, response=response
    )
    flash(msg, category="danger")
