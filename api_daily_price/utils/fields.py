from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('price_date')
parser.add_argument('open_price')
parser.add_argument('high_price')
parser.add_argument('low_price')
parser.add_argument('close_price')
parser.add_argument('name')
parser.add_argument('username')