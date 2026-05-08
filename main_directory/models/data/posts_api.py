from urllib import request

import flask
from flask_restful import reqparse, abort, Api, Resource
import base64

from . import db_session
from .posts import Post

blueprint = flask.Blueprint(
    'post_api',
    __name__,
    template_folder='templates'
)



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
        return flask.jsonify({'post': post.to_dict(only=('id', 'title', 'content', 'likes_amount', 'user_id', 'created_at', 'image'))})

    def delete(self, post_id):
        abort_if_post_not_found(post_id)
        session = db_session.create_session()
        posts = session.get(Post, post_id)
        session.delete(posts)
        session.commit()
        return flask.jsonify({'success': 'OK'})


parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('content', required=True)
parser.add_argument('image', required=True) # !!!биты предадутся в виде строки!!!
parser.add_argument('user_id', required=True, type=int)
parser.add_argument('image_type', required=True)

class PostListResource(Resource):
    def get(self):
        session = db_session.create_session()
        posts = session.query(Post).all()

        return flask.jsonify({'posts': [item.to_dict(only=('id', 'title', 'content', 'likes_amount', 'user_id', 'created_at', 'image')) for item in posts]})

    def post(self):
        print("qqq")
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
