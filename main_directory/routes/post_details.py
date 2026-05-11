import requests
from flask import Blueprint, render_template

detail_router = Blueprint("detail_router", __name__)


@detail_router.route("/details/<int:post_id>")
def show_post(post_id):
    return render_template('post_details.html',
                           post=requests.get(f"http://127.0.0.1:5000/api/posts/{post_id}").json()['post'])
