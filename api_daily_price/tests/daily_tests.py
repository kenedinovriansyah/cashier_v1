import unittest
from flask_api import status
from api_user.tests.user_test import readmes, readme
from api_server.server import create_app
from core.logger import logger
from faker import Faker
from datetime import datetime
from api_database.daily_price import DailyPrice

faker = Faker()

app = create_app()
count = None
with app.app_context():
    count = DailyPrice.query.count()

class DailyTests(unittest.TestCase):
    def setUp(self):
        self.e = None
        with app.test_client() as client:
            self.e = client

    def test_daily(self):
        logger.critical("Daily Tests")

    @unittest.skipIf(not readme or not readmes, 'token is expires')
    def test_daily_create(self):
        with app.app_context():
            response = self.e.post('/api/v1/daily/price/', data={
                'name': faker.name(),
                'price_date': datetime.utcnow(),
                'open_price': faker.random_number(),
                'high_price': faker.random_number(),
                'low_price': faker.random_number(),
                'close_price': faker.random_number()
            },headers={
                'Authorization': 'Bearer ' + readme,
                'x-token-api': 'Bearer ' + readmes
            })
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertNotEqual(response.data, None)
            logger.info("Daily Create")

    @unittest.skipIf(not readme or not readmes, 'token is expires')
    def test_daily_get_all(self):
        with app.app_context():
            response = self.e.get('/api/v1/daily/price/', headers={
                'Authorization': 'Bearer ' + readme,
                'x-token-api': 'Bearer ' + readmes
            })
            self.assertEqual(response.status_code,status.HTTP_200_OK)
            self.assertNotEqual(response.data,None)
            self.assertNotEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
            logger.info("Daily Get All")

    @unittest.skipIf(not readme or not readmes or not count, "token is expires or daily price not have data")
    def test_daily_get_detail(self):
        with app.app_context():
            data = DailyPrice.query.first()
            response = self.e.get('/api/v1/daily/price/%s/' % data.id)
            self.assertEqual(response.status_code,status.HTTP_200_OK)
            self.assertNotEqual(response.data, None)
            self.assertNotEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
            logger.info("Daily Price Detail")

