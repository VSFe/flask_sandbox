from flask_restx import Api
from app.service.user import user
from app.service.board import board
from app.service.article import article

rest_api = Api()

rest_api.add_namespace(user, '/user')
rest_api.add_namespace(board, '/board')
rest_api.add_namespace(article, '/article')