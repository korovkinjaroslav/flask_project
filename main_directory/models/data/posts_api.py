from random import seed
from urllib import request

import flask
from flask_restful import reqparse, abort, Api, Resource
from sqlalchemy import desc
import base64

from . import db_session
from .comments import Comment
from .likes import Like
from .posts import Post
from .users import User

blueprint = flask.Blueprint(
    'post_api',
    __name__,
    template_folder='templates'
)

POSTS_ON_PAGE_LIMIT = 10


def abort_if_post_not_found(post_id):
    session = db_session.create_session()
    posts = session.get(Post, post_id)
    if not posts:
        abort(404, message=f"Post {post_id} not found")


class PostResource(Resource):
    def get(self, post_id):
        abort_if_post_not_found(post_id)
        session = db_session.create_session()
        post = session.get(Post, post_id)
        d = {'post': post.to_dict(only=('id', 'title', 'content', 'likes_amount', 'user_id', 'created_at', 'image'))}
        d['post']['author'] = session.get(User, d['post']["user_id"]).username
        return flask.jsonify(d)


parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('content', required=True)
parser.add_argument('image', required=True)  # !!!биты предадутся в виде строки!!!
parser.add_argument('user_id', required=True, type=int)
parser.add_argument('image_type', required=True)


class PostListResource(Resource):
    def get(self):
        session = db_session.create_session()
        posts = session.query(Post).all()

        return flask.jsonify({'posts': [
            item.to_dict(only=('id', 'title', 'content', 'likes_amount', 'user_id', 'created_at', 'image')) for item in
            posts]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        new_post = Post(
            title=args['title'],
            content=args['content'],
            image=args['image'],
            user_id=args["user_id"],
        )
        session.add(new_post)
        session.commit()
        return flask.jsonify({'id': new_post.id})


class GetPosts(Resource):
    def get(self, first_post):
        res = {'posts': []}
        sess = db_session.create_session()
        posts = sess.query(Post).filter(Post.id <= first_post).order_by(desc(Post.id)).limit(POSTS_ON_PAGE_LIMIT)
        n = posts.count()
        if n == 0:
            res['first_post_of_next_page'] = 0
        else:
            res['first_post_of_next_page'] = posts[n - 1].id - 1
        for post in posts:
            res['posts'].append(
                post.to_dict(only=('id', 'title', 'content', 'likes_amount', 'user_id', 'created_at', 'image')))
            res['posts'][-1]["author"] = sess.get(User, res['posts'][-1]["user_id"]).username
        return flask.jsonify(res)


class DeletePost(Resource):
    def post(self, post_id):
        user_id = flask.session.get('_user_id')
        if user_id is None:
            return {"success": False}
        sess = db_session.create_session()
        post = sess.get(Post, post_id)
        user = sess.get(User, user_id)
        if user.status or int(user_id) == post.user_id:
            sess.query(Like).filter(Like.post_id == post_id).delete()
            sess.query(Comment).filter(Comment.post_id == post_id).delete()
            sess.delete(post)
            sess.commit()
            return {"success": True}
        else:
            return {"success": False}
