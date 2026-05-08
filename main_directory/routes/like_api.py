import flask
from flask_restful import reqparse, abort, Api, Resource

blueprint = flask.Blueprint(
    'post_api',
    __name__,
    template_folder='templates'
)


class LikePost(Resource):
    def post(self, post_id):
        return {
            "success": True,
            "likes": 123
        }
