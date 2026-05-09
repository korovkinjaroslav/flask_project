from tempfile import template

from flask import Blueprint, render_template, session

import requests
import json

from werkzeug.utils import redirect

from main_directory.models.data import posts

main_router = Blueprint("main_router", __name__)


@main_router.route("/")
def start():
    return redirect("/1")


@main_router.route("/<int:page_number>")
def main_page(page_number):
    return render_template('main_page.html', posts=requests.get(
        "http://127.0.0.1:5000/api/posts"
    ).json())
