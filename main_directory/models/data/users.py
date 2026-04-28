import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

USER_STATUS_USER = "user"
USER_STATUS_ADMIN = "admin"


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    DEFAULT_STATUS = USER_STATUS_USER
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True, index=True)
    username = sqlalchemy.Column(sqlalchemy.String,
                                 nullable=False, unique=True)
    password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    status = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=False,
        default=USER_STATUS_USER,
    )
    created_at = sqlalchemy.Column(
        sqlalchemy.DateTime, default=datetime.datetime.now)

    likes = orm.relationship("Like", back_populates="user", cascade="all, delete-orphan")
    comments = orm.relationship("Comment", back_populates="user", cascade="all, delete-orphan")
    posts = orm.relationship("Post", back_populates="user", cascade="all, delete-orphan")

    def set_password(self, password: str) -> None:
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def is_admin(self) -> bool:
        return self.status == USER_STATUS_ADMIN
