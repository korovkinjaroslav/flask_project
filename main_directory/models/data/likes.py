import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Like(SqlAlchemyBase):
    __tablename__ = 'likes'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"),
                                nullable=False)
    user = orm.relationship('User', back_populates="likes")
    post_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("posts.id"),
                                nullable=False)
    post = orm.relationship("Post", back_populates="likes")
