from core.extensions import db
from uuid import uuid4
from datetime import datetime

from decimal import Decimal as D
import sqlalchemy.types as types

class SqliteNumeric(types.TypeDecorator):
    impl = types.String
    def load_dialect_impl(self, dialect):
        return dialect.type_descriptor(types.VARCHAR(100))
    def process_bind_param(self, value, dialect):
        return str(value)
    def process_result_value(self, value, dialect):
        return D(value)

class DailyPrice(db.Model):
    __tablename__ = "tb_daily_price"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(225), unique=True, nullable=False,default=str(uuid4()))
    price_date = db.Column(db.DateTime,nullable=False)
    createAt = db.Column(db.DateTime, default=datetime.utcnow())
    updateAt = db.Column(db.DateTime, nullable=False)
    open_price = db.Column(SqliteNumeric(11,2), nullable=False)
    high_price = db.Column(SqliteNumeric(11,2), nullable=False)
    low_price = db.Column(SqliteNumeric(11,2), nullable=False)
    close_price = db.Column(SqliteNumeric(11,2), nullable=False)
    vendor = db.relationship('Vendor', backref="daily_price", lazy=True, cascade="all, delete-orphan")
    users_id = db.Column(db.Integer, db.ForeignKey("tb_user.id"), nullable=False)

class Vendor(db.Model):
    __tablename__ = "tb_vendor"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    createAt = db.Column(db.DateTime, default=datetime.utcnow())
    updateAt = db.Column(db.DateTime, nullable=False)
    daily_price_id = db.Column(db.Integer, db.ForeignKey("tb_daily_price.id"), nullable=False)
    