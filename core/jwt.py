from jwcrypto import jwk, jwt
from flask_api import status
from flask import jsonify, request
from functools import wraps
import ast
import json

class JsonWebToken:
    def generate(instance):
        key = jwk.JWK(generate="oct", size=256)
        key.export()
        token = jwt.JWT(header={'alg': 'HS256'}, claims={'user': str(instance.username)})
        token.make_signed_token(key)
        etoken = jwt.JWT(header={'alg': 'A256KW', 'enc': 'A256CBC-HS512'}, claims=token.serialize())
        etoken.make_encrypted_token(key)
        res = jsonify({
            'token': etoken.serialize(),
            'x-token-api': key
        })
        res.status = status.HTTP_200_OK
        return res

    def verify(f):
        @wraps(f)
        def decorators(*args,**kwargs):
            _t = request.headers['Authorization']
            _x = request.headers['x-token-api']
            if not _t or not _x:
                res = jsonify({
                    'message': 'Token is missing'
                })
                res.status = status.HTTP_400_BAD_REQUEST
                return res
            try:
                _x = ast.literal_eval(json.loads(json.dumps(_x.split('Bearer ')[1])))
                key = jwk.JWK(**_x)
                et = jwt.JWT(key=key,jwt=u"{}".format(_t.split("Bearer ")[1]))
                st = jwt.JWT(key=key, jwt=et.claims)
                res = jsonify(st.claims)
                res.status = status.HTTP_200_OK
                return res
            except ValueError:
                res = jsonify({
                    'message': 'Token is invalid'
                })
                res.status = status.HTTP_400_BAD_REQUEST
                return res
            return f(*args,**kwargs)
        return decorators
