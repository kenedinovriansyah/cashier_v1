from datetime import datetime
from api_database.user import User
from api_user.utils.fields import parser
from core.extensions import db
from flask import jsonify, make_response
from flask_api import status
from flask_restful import Resource
from werkzeug.security import generate_password_hash


class UserAPIView(Resource):

    def get(self):
        return jsonify({
            'message': 'Get getall'
        })
    
    def post(self):
        req = parser.parse_args()
        check = User.query.filter((User.username == req.get('username')) | (User.email == req.get('email'))).first()
        if check:
            res = jsonify({
                'message': 'Username or email already exists'
            })
            res.status = status.HTTP_400_BAD_REQUEST
            return res
        db.session.add(
            User(
                username=req.get('username'),
                email=req.get('email'),
                password=generate_password_hash(req.get('password')),
                updateAt=datetime.utcnow()
            )
        )
        db.session.commit()
        res = jsonify({
            'message': 'Accounts has been created'
        })
        res.status = status.HTTP_201_CREATED
        return res
