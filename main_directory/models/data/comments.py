import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Comment(SqlAlchemyBase):
    __tablename__ = 'comments'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"),
                                nullable=False)
    user = orm.relationship('User')
    post_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    # НАДО БУДЕТ ФОРЕЙН КЕЙ ДЛЯ ПОСТА СДЕЛАТЬ ОБЯЗАТЕЛЬНО!!!
    created_at = sqlalchemy.Column(
        sqlalchemy.DateTime, default=datetime.datetime.now)
