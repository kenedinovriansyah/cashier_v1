from flask import jsonify
from flask_api import status
from flask_restful import Resource
from core.jwt import JsonWebToken
from api_database.user import User
from api_user.utils.fields import parser
from werkzeug.security import check_password_hash

class AuthToken(Resource):
    def post(self):
        req = parser.parse_args()
        check = User.query.filter_by(username=req.get('username')).first()
        if not check_password_hash(check.password,req.get('password')):
            res = jsonify({
                'message': 'Incorrect username or password'
            })
            res.status = status.HTTP_400_BAD_REQUEST
            return res
        return JsonWebToken.generate(check)

class VerifyToken(Resource):

    @JsonWebToken.verify
    def post(self):
        return jsonify({
            'message': 'token'
        })
