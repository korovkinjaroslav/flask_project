from flask import Blueprint, render_template
from flask_login import current_user

import requests

from werkzeug.utils import redirect

from main_directory.models.data import db_session
from main_directory.models.data.posts import Post

from sqlalchemy import desc

main_router = Blueprint("main_router", __name__)


@main_router.route("/")
def start():
    sess = db_session.create_session()
    fpost = sess.query(Post).order_by(desc(Post.id)).first()
    if fpost is None:
        if current_user.is_authenticated:
            return redirect("/create_post")
        return redirect("/login")
    print(fpost.id)
    return redirect(f"/main_page/{fpost.id}")


@main_router.route("/main_page/<int:first_post>")
def main_page(first_post):
    print(first_post)
    return render_template('main_page.html', posts=requests.get(
        f"http://127.0.0.1:5000/api/get_posts_from/{first_post}"
    ).json())
