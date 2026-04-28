from flask import Blueprint


main_router = Blueprint("main_router", __name__)


@main_router.route("/")
def start():
    return "developing"
