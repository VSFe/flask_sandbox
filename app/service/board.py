from flask import request, session
from flask_restx import Resource, Namespace, resource
from app.api.database import DB
from app.models.user import User
from app.models.board import Board
from app.api.serialize import to_serializable

board = Namespace(
    name="Board",
    description="게시판 관리를 위한 API"
)

@board.route('/create')
class BoardCreate(Resource):
    @board.expect(Board)
    @board.doc(responses={ 200 : 'Create Board Success'})
    @board.doc(responses={ 404 : 'User Not Found'})
    @board.doc(responses={ 409 : 'Create Failed'})
    @board.doc(responses={ 500 : 'Internal Server Error'})
    

    def post(self):
        try:
            user_email = session.get('user_email')
            
            if user_email is None:
                return {
                    "status" : "User Not Found"
                }, 404

            name = request.json['name']
            find_result = Board.query.filter_by(name=name).first()

            if find_result is not None:
                return {
                    "message" : "Create Failed."
                }, 409

            else:
                user_info = User.query.filter_by(email=user_email).first()\
                            .to_dict()['id']

                board_info = Board(name=name, owner=user_info)
                DB.session.add(board_info)
                DB.session.commit()
                return {
                    "message"   : "Create Board Success",
                    "board"     : to_serializable(board_info.to_dict())
                }, 200
        except:
            return {
                "message" : "Internal Server Error"
            }, 500
            
            
@board.route('/<string:board_name>')
class BoardRead(Resource):
    @board.expect(Board)
    @board.doc(responses={ 200 : 'Read Success'})
    @board.doc(responses={ 404 : 'Board Not Found'})
    @board.doc(responses={ 500 : 'Internal Server Error'})
    
    def get(self, board_name):       
        try:

            find_result = Board.query.filter_by(name=board_name).first()

            if find_result is None:
                return {
                    "message" : "Board Not Found."
                }, 404

            return {
                "message"   : "Read Success",
                "name"      : find_result.name,
                "articles"  : list(map(lambda x: to_serializable(x.to_dict()), find_result.articles_on_board))
            }, 200

        except:
            return {
                "message" : "Internal Server Error"
            }, 500


@board.route('/<string:board_name>/update')
class BoardUpdate(Resource):
    @board.expect(Board)
    @board.doc(responses={ 200 : 'Update Success'})
    @board.doc(responses={ 404 : 'Board Not Found'})
    @board.doc(responses={ 409 : 'Not Enough Permission'})
    @board.doc(responses={ 500 : 'Internal Server Error'})

    def post(self, board_name):
        try:
            name        = request.json['name']

            board_info = Board.query.filter_by(name=board_name).first()
            user_info = User.query.filter_by(email=session.get('user_email')).first()

            if board_info is None:
                return {
                    "status" : "Board Not Found."
                }, 404

            if user_info is None or user_info.to_dict()['id'] != board_info.to_dict()['owner']:
                return {
                    "status" : "Not Enough Permission"
                }, 409

            board_info.name = name
            DB.session.commit()

            return {
                "status" : "Update Success.",
                "update" : to_serializable(board_info)
            }, 200
        except:
            return {
                "status" : "Internal Server Error"
            }, 500

@board.route('/<string:board_name>/delete')
class BoardDelete(Resource):
    @board.expect(Board)
    @board.doc(responses={ 200 : 'Delete Success'})
    @board.doc(responses={ 404 : 'Board Not Found'})
    @board.doc(responses={ 409 : 'Not Enough Permission'})
    @board.doc(responses={ 409 : 'Board Has Articles'})
    @board.doc(responses={ 500 : 'Internal Server Error'})

    def delete(self, board_name):
        try:
            board_info  = Board.query.filter_by(name=board_name).first()
            user_info   = User.query.filter_by(email=session.get('user_email')).first()
            articles    = board_info.articles_on_board

            if board_info is None:
                return {
                    "status" : "Board Not Found."
                }, 404

            if user_info is None or user_info.to_dict()['id'] != board_info.to_dict()['owner']:
                return {
                    "status" : "Not Enough Permission"
                }, 409

            if len(articles) >= 1:
                return {
                    "status" : "Board Has Article(s)"
                }, 409

            DB.session.delete(board_info)
            DB.commit()

            return {
                "status" : "Delete Success."
            }, 200
        except:
            return {
                "status" : "Internal Server Error"
            }, 500