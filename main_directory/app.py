import os

from flask import Flask
from flask_login import LoginManager
from flask_restful import reqparse, abort, Api, Resource


from main_directory.models.data import db_session, posts_api
from main_directory.models.data.users import User
from main_directory.routes.auth import auth_router
from main_directory.routes.main import main_router

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(12)

api = Api(app)
api.add_resource(posts_api.PostResource, '/api/posts/<int:post_id>')
api.add_resource(posts_api.PostListResource, '/api/posts')

_db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", "db", "database.db")
db_session.global_init(_db_path)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, user_id)


app.register_blueprint(main_router)
app.register_blueprint(auth_router)


def main():
    app.run()


if __name__ == '__main__':
    main()
