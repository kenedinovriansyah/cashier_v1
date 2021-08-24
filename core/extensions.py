import os
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

basedir = os.path.abspath(os.path.dirname(__file__))


db = SQLAlchemy()
migrate = Migrate()
session = Session()
ma = Marshmallow()

from api_database import *

def ext(app):
    with app.app_context():
        from api_user.views.user import UserAPIView
        from api_user.views.authtoken import AuthToken, VerifyToken
        from api_daily_price.views.daily_price import DailyPriceAPIView, DailyPriceDetailAPIView
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, '../', 'database.sqlite')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(app)
        migrate.init_app(app,db,render_as_batch=True)
        session.init_app(app)
        ma.init_app(app)
        api = Api(app)
        api.add_resource(UserAPIView, '/api/v1/user/')
        api.add_resource(AuthToken, "/api/v1/user/login/")
        api.add_resource(VerifyToken, "/api/v1/user/verify/")
        api.add_resource(DailyPriceAPIView, "/api/v1/daily/price/")
        api.add_resource(DailyPriceDetailAPIView,"/api/v1/daily/price/<id>/")
