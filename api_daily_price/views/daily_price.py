from datetime import datetime

from api_daily_price.utils.fields import parser
from api_database.daily_price import DailyPrice, Vendor
from core.extensions import db
from core.jwt import JsonWebToken
from flask import jsonify, request
from flask_api import status
from flask_restful import Resource
from core.extensions import ma
from api_daily_price.utils.schema import DailySchema


class DailyPriceAPIView(Resource):
    def get(self):
        schema = DailySchema(many=True)
        data = schema.dump(DailyPrice.query.all())
        res = jsonify({'data': data})
        res.status = status.HTTP_200_OK
        return res

    def post(self):
        req = parser.parse_args()
        current_user = JsonWebToken.current_user(request.headers['Authorization'],request.headers['x-token-api'])
        if not current_user:
            res = jsonify({
                'message': 'Unauthorized'
            })
            res.status = status.HTTP_401_UNAUTHORIZED
            return res
        daily = DailyPrice(
                price_date=datetime.utcnow(),
                updateAt=datetime.utcnow(),
                open_price=req.get('open_price'),
                high_price=req.get('high_price'),
                low_price=req.get('low_price'),
                close_price=req.get('close_price'),
                users_id=current_user.id
            )
        db.session.add(
            daily
        )
        db.session.commit()
        db.session.add(
            Vendor(
                name=req.get('name'),
                updateAt=datetime.utcnow(),
                daily_price_id=daily.id
            )
        )
        db.session.commit()
        res = jsonify({
            'message': 'create'
        })
        res.status = status.HTTP_201_CREATED
        return res

class DailyPriceDetailAPIView(Resource):
    def post(self):
        res = jsonify({
            'message': 'Update'
        })
        res.status = status.HTTP_200_OK
        return res

    def get(self,id):
        schema = DailySchema()
        data = schema.dump(DailyPrice.query.filter_by(id=id).first())
        res = jsonify(data)
        res.status = status.HTTP_200_OK
        return res
