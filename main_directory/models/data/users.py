import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class User(SqlAlchemyBase):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True, index=True)
    username = sqlalchemy.Column(sqlalchemy.String,
                                 nullable=False)
    password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    status = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    created_at = sqlalchemy.Column(
        sqlalchemy.DateTime, default=datetime.datetime.now)

    likes = orm.relationship("Like", back_populates="user", cascade="all, delete-orphan")
    comments = orm.relationship("Comment", back_populates="user", cascade="all, delete-orphan")
    posts = orm.relationship("Post", back_populates="user", cascade="all, delete-orphan")
