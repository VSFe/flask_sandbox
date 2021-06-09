from sqlalchemy.sql import text
from app.api.database import DB
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, validate
from datetime import datetime

class Board(DB.Model):
    """
    table name: test_board

    table info
    - id: board id
    - name: board name
    - create_date: when this board was created
    - owner: board owner (FK: User.id, DISTINCT)
    """

    __tablename__   = 'test_board'
    __table_args__  = {'mysql_collate' : 'utf8_general_ci'}

    id                  = DB.Column(DB.Integer, primary_key=True, nullable=False, autoincrement=True)
    name                = DB.Column(DB.String(30), nullable=False)
    create_date         = DB.Column(DB.DateTime, default=datetime.utcnow())
    owner               = DB.Column(DB.Integer, DB.ForeignKey('test_user.id'))

    articles_on_board   = DB.relationship('Article', back_populates='boards')

    def __init__ (self, name, owner):
        self.name   = name
        self.owner  = owner

    def __repr__ (self):
        return 'board_name: {}, created_date: {}'.format(
            self.name, self.create_date
        )
        
    def to_dict (self):
        return {x.name: getattr(self, x.name) for x in self.__table__.columns}

    def serializable_dict (self):
        dict_ = self.to_dict()
        dict_['create_date'] = dict_['create_date'].isoformat()

        return dict_

