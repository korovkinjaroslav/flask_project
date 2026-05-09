from tempfile import template

from flask import Blueprint, render_template, session

import requests
import json

from werkzeug.utils import redirect

from main_directory.models.data import db_session
from main_directory.models.data.posts import Post

from sqlalchemy import desc

main_router = Blueprint("main_router", __name__)


@main_router.route("/")
def start():
    sess = db_session.create_session()
    fpost = sess.query(Post).order_by(desc(Post.id)).first()
    print(fpost.id)
    return redirect(f"/1/{fpost.id}")


"""TODO:
posts должен содержать author
нужно передавать индекс поста где заканчивается страница
 """


@main_router.route("/<int:page_number>/<int:first_post>")
def main_page(page_number, first_post):
    print(first_post)
    return render_template('main_page.html', posts=requests.get(
        f"http://127.0.0.1:5000/api/get_posts_from/{first_post}"
    ).json())
