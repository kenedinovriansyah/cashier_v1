from core.extensions import db
from datetime import datetime
from uuid import uuid4

class User(db.Model):
    __tablename__ = "tb_user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(255), nullable=False, unique=True,default=str(uuid4()))
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(225), nullable=False)
    createAt = db.Column(db.DateTime, default=datetime.utcnow())
    updateAt = db.Column(db.DateTime, nullable=False)
    daily_price = db.relationship("DailyPrice", backref="author", lazy=True, cascade="all,delete-orphan")