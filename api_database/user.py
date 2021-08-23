from core.extensions import db
from datetime import datetime

class User(db.Model):
    __table_name__ = "tb_user"
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.utcnow())
    update_at = db.Column(db.DateTime, nullable=False)