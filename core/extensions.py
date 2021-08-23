import os

from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))


db = SQLAlchemy()
migrate = Migrate()

from api_database.user import User


def ext(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, '../', 'database.sqlite')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    migrate.init_app(app,db)
    api = Api(app)
    from api_user.views.user import UserAPIView
    from api_user.views.authtoken import AuthToken, VerifyToken
    api.add_resource(UserAPIView, '/api/v1/user/')
    api.add_resource(AuthToken, "/api/v1/user/login/")
    api.add_resource(VerifyToken, "/api/v1/user/verify/")
