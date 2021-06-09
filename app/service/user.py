import jwt
import bcrypt
from flask import request, session
from flask_restx import Resource, Namespace
from app.api.database import DB
from app.models.user import User

user = Namespace(
    name="User",
    description="사용자 회원가입 및 로그인을 위한 API"
)

@user.route('/signup')
class UserSignup(Resource):
    @user.expect(User)
    @user.doc(responses={ 200 : 'Signup Success' })
    @user.doc(responses={ 409 : 'Signup Failed' })
    @user.doc(responses={ 500 : 'Internal Server Error' })

    def post(self):
        fullname    = request.json['fullname']
        email       = request.json['email']
        password    = request.json['password']

        find_result = User.query.filter_by(email=email).first()

        if find_result is not None:
            return {
                "message" : "Register Failed."
            }, 409

        try:
            password_secret = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            user_info = User(fullname=fullname,
                            password=password_secret, email=email)
            DB.session.add(user_info)
            DB.session.commit()
            
            return {
                "message"       : "Register Success.",
                "Authroization" : jwt.encode({ 'email' : email }, "secret", algorithm='HS256')
            }, 200

        except Exception as e:
            print(e)
            return {
                "message" : "Internal Server Error.",
            }, 500
        

@user.route('/login')
class UserLogin(Resource):
    @user.expect(User)
    @user.doc(responses={ 200 : 'Login Success' })
    @user.doc(responses={ 404 : 'User Not Found' })
    @user.doc(responses={ 409 : 'Login Failed' })
    @user.doc(responses={ 500 : 'Internal Server Error' })
    
    def post(self):
        email       = request.json['email']
        password    = request.json['password']

        user_data = User.query.filter_by(email=email).first()

        if not user_data:
            return {
                "message" : "User Not Found."
            }, 404
        elif not bcrypt.checkpw(password.encode('utf-8'), user_data.password_secret.encode('utf-8')):
            return {
                "message" : "Login Failed."
            }, 409

        try:
            session.clear()
            session['user_email'] = email

            return {
                "message" : "Login Success",
                "Authroization" : jwt.encode({ 'email' : email }, "secret", algorithm='HS256')
            }, 200
        except:
            return {
                "message" : "Internal Server Error"
            }, 500

@user.route('/logout')
class UserLogout(Resource):
    @user.doc(responses={ 200 : 'Login Success' })
    @user.doc(responses={ 404 : 'Not Logged in' })
    @user.doc(responses={ 500 : 'Internal Server Error' })
    def get(self):
        if 'user_email' not in session:
            return {
                "status" : "Not Logged in"
            }, 404
        else:
            try:
                session.clear()
                return {
                    "status" : "Logout Success."
                }, 200
            except:
                return {
                    "status" : "Logout Failed."
                }, 500


@user.route('/info')
class UserInfo(Resource):
    @user.doc(responses={ 200 : 'Success' })
    @user.doc(responses={ 500 : 'Internal Server Error' })
    def get(self):
        try:
            user_email = session.get('user_email')
            if user_email is None:
                return {
                    "status" : "Not Loggined"
                }, 200
            else:
                return {
                    "status"    : "Loggedin",
                    "fullname"  : User.query.filter_by(email=user_email).first().fullname,
                    "email"     : user_email
                }, 200
        except Exception as e:
            print(e)
            return {
                "status" : "Internal Server Error"
            }, 500
    