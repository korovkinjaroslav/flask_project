import flask
from flask_restful import reqparse, abort, Api, Resource
from main_directory.models.data import db_session
from main_directory.models.data.posts import Post
from main_directory.models.data.likes import Like

blueprint = flask.Blueprint(
    'post_api',
    __name__,
    template_folder='templates'
)


def abort_if_post_not_found(post_id):
    session = db_session.create_session()
    posts = session.get(Post, post_id)
    if not posts:
        abort(404, message=f"Пост, который вы лайкули, был удален")


class LikePost(Resource):
    def post(self, post_id):
        if flask.session.get('_user_id') is None:
            return {"success": False,
                    "problem": "ВЫ НЕ ЗАРЕГИСТРИРОВАНЫ"}
        abort_if_post_not_found(post_id)
        user_id = flask.session.get('_user_id')
        db_sess = db_session.create_session()
        post = db_sess.get(Post, post_id)
        post.likes_amount = post.likes_amount + 1
        likes_amount = post.likes_amount
        like = Like()
        like.user_id = user_id
        like.post_id = post_id
        db_sess.add(like)
        db_sess.commit()
        return {"success": True,
                "likes": likes_amount}


class RemoveLike(Resource):
    def post(self, post_id):
        if flask.session.get('_user_id') is None:
            return {"success": False,
                    "problem": "ВЫ НЕ ЗАРЕГИСТРИРОВАНЫ"}
        abort_if_post_not_found(post_id)
        abort_if_post_not_found(post_id)
        user_id = flask.session.get('_user_id')
        db_sess = db_session.create_session()
        post = db_sess.get(Post, post_id)
        post.likes_amount = post.likes_amount - 1
        likes_amount = post.likes_amount
        like = db_sess.query(Like).filter(Like.post_id == post_id, Like.user_id == user_id).first()
        db_sess.delete(like)
        db_sess.commit()
        return {"success": True,
                "likes": likes_amount}


class CheckLike(Resource):
    def get(self, post_id):
        print(12345)
        user_id = flask.session.get('_user_id')
        if user_id is None:
            return {"exists": False}
        sess = db_session.create_session()
        like = sess.query(Like).filter(Like.post_id == post_id, Like.user_id == user_id).first()
        if like is None:
            return {"exists": False}
        return {"exists": True}
