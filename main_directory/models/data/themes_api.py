import flask
from flask_restful import reqparse, abort, Api, Resource
from sqlalchemy import desc
import base64

from . import db_session
from .posts import Post
from .themes import Theme

blueprint = flask.Blueprint(
    'themes_api',
    __name__,
    template_folder='templates'
)

class GetAllThemes(Resource):
    def get(self):
        sess = db_session.create_session()
        all_themes = sess.query(Theme).all()
        d = {
            'themes':[item.to_dict(only=('id', 'title')) for item in all_themes]
        }
        for i in range(len(d['themes'])):
            d['themes'][i]["amount_of_posts"] = sess.query(Post).filter(Post.theme_id == d['themes'][i]['id']).count()
        return flask.jsonify(d)