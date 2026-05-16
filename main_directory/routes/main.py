from flask import Blueprint, render_template, session
from flask_login import current_user

import requests, os

from werkzeug.utils import redirect

from main_directory.models.data import db_session, themes
from main_directory.models.data.posts import Post
from main_directory.models.data.users import User

from sqlalchemy import desc

main_router = Blueprint("main_router", __name__)

BASE_URL = os.getenv('BASE_URL', 'http://localhost:5000')


@main_router.route("/")
def start():
    return render_template("start_page.html",
                           themes=requests.get(f"{BASE_URL}/api/themes").json())


@main_router.route("/main_page/<int:theme>")
def redirect_to_main(theme):
    sess = db_session.create_session()
    fpost = sess.query(Post).filter(Post.theme_id == theme).order_by(desc(Post.id)).first()
    """if fpost is None:
        if current_user.is_authenticated:
            return redirect("/create_post")
        return redirect("/login")
    print(fpost.id)"""
    if fpost is None:
        return redirect(f"/main_page/{theme}/0")
    return redirect(f"/main_page/{theme}/{fpost.id}")


@main_router.route("/main_page/<string:theme>/<int:first_post>")
def main_page(theme, first_post):
    print(session.get('_user_id'))
    print(f"{BASE_URL}/api/get_posts_from/{first_post}")
    if session.get("_user_id") == None:
        is_admin = False
    else:
        is_admin = db_session.create_session().get(User, session.get('_user_id')).status
    return render_template('main_page.html', posts=requests.get(
        f"{BASE_URL}/api/get_posts_from/{theme}/{first_post}"
    ).json(), is_admin=is_admin, theme=theme)
