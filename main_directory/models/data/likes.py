import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Like(SqlAlchemyBase):
    __tablename__ = 'likes'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("users.id"),
                                nullable=False)
    user = orm.relationship('User')
    post_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    # НАДО БУДЕТ ФОРЕЙН КЕЙ ДЛЯ ПОСТА СДЕЛАТЬ ОБЯЗАТЕЛЬНО!!!
