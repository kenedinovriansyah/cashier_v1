from core.extensions import ma
from marshmallow import fields

class DailySchema(ma.Schema):
    id = fields.Str()
    public_id = fields.Str()
    price_date = fields.Str()
    createAt = fields.Str()
    updateAt = fields.Str()
    open_price = fields.Str()
    high_price = fields.Str()
    low_price = fields.Str()
    close_price = fields.Str()
    vendor = fields.Str()
    users_id = fields.Str()

