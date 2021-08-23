import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api

db = SQLAlchemy()
migrate = Migrate()

basedir = os.path.abspath(os.path.dirname(__name__))

import api_database

def ext(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL") or "sqlite:///" + os.path.join(basedir, "database.sqlite")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    migrate.init_app(app,db)
    api = Api(app)
    from api_user.views.user import UserAPIView, AuthToken, VerifyToken, RefreshToken
    api.add_resource(UserAPIView, "/api/v1/user/")
    api.add_resource(AuthToken, "/api/v1/user/login/")
    api.add_resource(RefreshToken, "/api/v1/user/refresh/")
    api.add_resource(VerifyToken, "/api/v1/user/verify/")