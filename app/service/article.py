from app.api.serialize import to_serializable
from flask import request, session
from flask_restx import Resource, Namespace
from app.api.database import DB
from app.models.user import User
from app.models.board import Board
from app.models.article import Article

article = Namespace(
    name="Article",
    description="게시물 업로드 및 관리를 위한 API"
)

@article.route('/<string:board_name>/create')
class ArticleCreate(Resource):
    @article.expect(Article)
    @article.doc(responses={ 200 : 'Create Article Success'})
    @article.doc(responses={ 404 : 'Board Not Found'})
    @article.doc(responses={ 409 : 'Not Enough Permission'})
    @article.doc(responses={ 500 : 'Internal Server Error'})

    def post(self, board_name):
        try:
            user_email = session.get('user_email')
            board_info = Board.query.filter_by(name=board_name).first()
            
            if board_info is None:
                return {
                    "status" : "Board Not Found."
                }, 404

            if user_email is None:
                return {
                    "status" : "Not Enough Permission"
                }, 409
            
            title           = request.json['title']
            content         = request.json['content']
            user_info       = User.query.filter_by(email=user_email).first()\
                            .to_dict()['id']
            board_idx       = board_info.id

            article_info    = Article(title=title, content=content, writter=user_info, board=board_idx)

            DB.session.add(article_info)
            DB.session.commit()

            return {
                "status"    : "Create Article Success.",
                "article"   : to_serializable(article_info.to_dict())
            }, 200

        except:
            return {
                "status" : "Internal Server Error",
            }, 500


@article.route('/<string:board_name>/<int:article_id>')
class ArticleRead(Resource):
    @article.expect(Article)
    @article.doc(responses={ 200 : 'Read Article Success'})
    @article.doc(responses={ 404 : 'Article Not Found'})
    @article.doc(responses={ 500 : 'Internal Server Error'})

    def get(self, board_name, article_id):
        try:

            board_info      = Board.query.filter_by(name=board_name).first()
            article_info    = Article.query.filter_by(id=article_id).first()

            if board_info is None or article_info is None or \
                article_info.board != board_info.id:
                return {
                    "status" : "Article Not Found."
                }, 404

            return {
                "status"    : "Search Success",
                "title"     : article_info.title,
                "content"   : article_info.content
            }, 200

        except:
            return {
                "status" : "Internal Server Error"
            }, 500
        

@article.route('/<string:board_name>/<int:article_id>/update')
class ArticleUpdate(Resource):
    @article.expect(Article)
    @article.doc(responses={ 200 : 'Update Article Success'})
    @article.doc(responses={ 404 : 'Article Not Found'})
    @article.doc(responses={ 409 : 'Not Enough Permission'})
    @article.doc(responses={ 500 : 'Internal Server Error'})

    def post(self, board_name, article_id):
        try:
            user_email      = session.get('user_email')
            title           = request.json['title']
            content         = request.json['content']
            board_info      = Board.query.filter_by(name=board_name).first()
            article_info    = Article.query.filter_by(id=article_id).first()

            if board_info is None or article_info is None or \
                article_info.board != board_info.id:
                return {
                    "status" : "Article Not Found."
                }, 404

            if user_email is None or \
                User.query.filter_by(email=user_email).first().id != article_info.writter:
                return {
                    "status" : "Not Enough Permission"
                }, 409
            

            article_info.title   = title
            article_info.content = content

            DB.session.commit()

            return {
                "status"    : "Update Article Success",
                "article"   : to_serializable(article_info.to_dict())
            }, 200
        except:
            return {
                "status"    : "Internal Server Error"
            }, 500
        


@article.route('/<string:board_name>/<int:article_id>/delete')
class ArticleDelete(Resource):
    @article.expect(Article)
    @article.doc(responses={ 200 : 'Delete Article Success'})
    @article.doc(responses={ 404 : 'Article Not Found'})
    @article.doc(responses={ 409 : 'Not Enough Permission'})
    @article.doc(responses={ 500 : 'Internal Server Error'})

    def delete(self, board_name, article_id):
        user_email      = session.get('user_email')
        board_info      = Board.query.filter_by(name=board_name).first()
        article_info    = Article.query.filter_by(id=article_id).first()
        
        if user_email is None or \
            User.query.filter_by(email=user_email).first().id != article_info.writter:
            return {
                "status" : "Not Enough Permission"
            }, 409

        if board_info is None or article_info is None or \
            article_info.board != board_info.id:
            return {
                "status" : "Article Not Found."
            }, 404

        DB.session.delete(article_info)
        session.commit()