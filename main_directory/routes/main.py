from tempfile import template

from flask import Blueprint, render_template

import requests
import json

from main_directory.models.data import posts

main_router = Blueprint("main_router", __name__)


@main_router.route("/")
def start():
    return render_template('main_page.html', posts=requests.get(
        "http://127.0.0.1:5000/api/posts"
    ).json())
