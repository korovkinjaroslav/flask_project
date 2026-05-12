from flask import session

from . import db_session
from .comments import Comment
from .users import User

from flask_restful import reqparse, abort, Api, Resource


class DeleteComment(Resource):
    def post(self, comment_id):
        user_id = session.get("_user_id")
        sess = db_session.create_session()
        if user_id is None:
            return {"success": False}
        user = sess.get(User, user_id)
        comment = sess.get(Comment, comment_id)
        if user.status or comment.user_id == user.id:
            sess.delete(comment)
            sess.commit()
            return {"seccess": True}
        return {"success": False}
