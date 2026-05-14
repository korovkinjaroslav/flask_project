import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase

class Theme(SqlAlchemyBase):
    __tablename__ = 'themes'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    posts = orm.relationship("Post", back_populates="theme")
