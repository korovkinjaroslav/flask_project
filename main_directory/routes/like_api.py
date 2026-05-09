import flask
from flask_restful import reqparse, abort, Api, Resource

blueprint = flask.Blueprint(
    'post_api',
    __name__,
    template_folder='templates'
)


class LikePost(Resource):
    def post(self, post_id):
        if flask.session.get('_user_id') is None:
            return {"success": False,
                    "problem": "ВЫ НЕ ЗАРЕГИСТРИРОВАНЫ"}
        return {
            "success": True,
            "likes": 123
        }
