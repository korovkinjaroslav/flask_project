import os

from flask import Flask
from flask_login import LoginManager
from flask_restful import reqparse, abort, Api, Resource


from main_directory.models.data import db_session, posts_api
from main_directory.models.data.users import User
from main_directory.routes.auth import auth_router
from main_directory.routes.main import main_router
from main_directory.routes import like_api
from main_directory.routes.post_details import detail_router
from main_directory.routes.create_post import create_post_router


import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(12)
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365
)

api = Api(app)
api.add_resource(posts_api.PostResource, '/api/posts/<int:post_id>')
api.add_resource(posts_api.PostListResource, '/api/posts')
api.add_resource(posts_api.GetPosts, '/api/get_posts_from/<int:first_post>')
api.add_resource(like_api.LikePost, '/api/like/<int:post_id>')
api.add_resource(like_api.RemoveLike, '/api/remove_like/<int:post_id>')
api.add_resource(like_api.CheckLike, '/api/check_like/<int:post_id>')

_db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", "db", "database.db")
db_session.global_init(_db_path)


@app.teardown_appcontext
def shutdown_db_session(exception):
    db_session.remove_session()


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth_router.login'
@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, user_id)


app.register_blueprint(main_router)
app.register_blueprint(auth_router)
app.register_blueprint(detail_router)
app.register_blueprint(create_post_router)


def main():
    app.run()


if __name__ == '__main__':
    main()
