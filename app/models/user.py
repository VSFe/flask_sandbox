from sqlalchemy.sql import text
from app.api.database import DB
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, validate
from datetime import datetime

class User(DB.Model):
    """
    table name: test_user
    
    table info
    - id: user id
    - fullname: user name
    - password_secret: encoded password
    - email: user email
    - registration_date: when this user was registrated
    """

    __tablename__   = 'test_user'
    __table_args__  = {'mysql_collate' : 'utf8_general_ci'}

    id                  = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    fullname            = DB.Column(DB.String(30), nullable=False)
    password_secret     = DB.Column(DB.String(100), nullable=False)
    email               = DB.Column(DB.String(40), nullable=False, unique=True)
    registration_date   = DB.Column(DB.DateTime, default=datetime.utcnow())

    articles_on_users   = DB.relationship('Article', back_populates='users')

    def __init__ (self, fullname, password, email):
        self.fullname           = fullname
        self.password_secret    = password
        self.email              = email

    def __repr__ (self):
        return 'user_name: {}, email: {}, registration_date: {}'.format(
            self.fullname, self.email, self.registration_date
        )
        
    def to_dict (self):
         return {x.name: getattr(self, x.name) for x in self.__table__.columns}