from flask import jsonify
from flask_restful import Resource, reqparse
from api_database.user import User
from werkzeug.security import check_password_hash, generate_password_hash
from core.extensions import db
from datetime import datetime

parser = reqparse.RequestParser()
parser.add_argument("username")
parser.add_argument("email")
parser.add_argument("password")
class UserAPIView(Resource):
    def get(self):
        return {"message": "Hello Worlds"}

    def post(self):
        req = parser.parse_args()
        db.session.add(User(
            username=req.get('username'),
            email=req.get('email'),
            password=generate_password_hash(req.get('password')),
            update_at=datetime.utcnow()
        ))
        db.session.commit()
        return jsonify({
            'message': 'Hello Worlds'
        })

class AuthToken(Resource):
    def post(self):
        return {'message': "login"}

class RefreshToken(Resource):
    def post(self):
        return {'message': 'refresh'}

class VerifyToken(Resource):
    def post(self):
        return {'message': 'verify'}
