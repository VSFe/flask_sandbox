from sqlalchemy.sql import text
from app.api.database import DB
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, validate
from datetime import datetime


class Article(DB.Model):
    """
    table name: test_article

    table info
    - id: article id
    - title: article title
    - content: article content
    - create_date: 
    - writter: user who writes article (FK: User.id)
    - board: board where written this article (FK: Board.id)
    """


    __tablename__   = 'test_article'
    __table_args__  = {'mysql_collate' : 'utf8_general_ci'}

    id          = DB.Column(DB.Integer, primary_key=True, nullable=False, autoincrement=True)
    title       = DB.Column(DB.String(50), nullable=False)
    content     = DB.Column(DB.Text(), nullable=False)
    create_date = DB.Column(DB.DateTime, default=datetime.utcnow())
    writter     = DB.Column(DB.Integer, DB.ForeignKey('test_user.id'), nullable=False)
    board       = DB.Column(DB.Integer, DB.ForeignKey('test_board.id'), nullable=False)
    
    boards      = DB.relationship('Board', back_populates='articles_on_board')
    users       = DB.relationship('User', back_populates='articles_on_users')


    def __init__ (self, title, content, writter, board):
        self.title   = title
        self.content = content
        self.writter = writter
        self.board   = board

    def to_dict (self):
        return {x.name: getattr(self, x.name) for x in self.__table__.columns}

    def serializable_dict (self):
        dict_ = self.to_dict()
        dict_['create_date'] = dict_['create_date'].isoformat()

        return dict_