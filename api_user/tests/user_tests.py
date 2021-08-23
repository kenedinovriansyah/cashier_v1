from api_database.user import User
import unittest
from flask_api import status
from faker import Faker
from api_server.server import create_app
from core.logger import logger
from core.extensions import db, basedir
import os
from api_database.user import User

faker = Faker()

app = create_app()
exists = None
with app.app_context():
    exists = User.query.count()

class UserTests(unittest.TestCase):
    def setUp(self):
        with app.test_client() as client:
            self.e = client

    def test_user(self):
        logger.critical("User Tests")

    @unittest.skipIf(exists == 0, "user not have data")
    def test_user_login(self):
        with app.app_context():
            print(User.query.all())
            response = self.e.post("/api/v1/user/login/")
            self.assertEqual(response.status_code,status.HTTP_200_OK)
            self.assertNotEqual(response.data, None)
            logger.info("User Login")
    
    def test_user_refresh_token(self):
        with app.app_context():
            response = self.e.post("/api/v1/user/refresh/")
            self.assertEqual(response.status_code,status.HTTP_200_OK)
            self.assertNotEqual(response.data, None)
            logger.info("Refresh Token")

    def test_user_verify_token(self):
        with app.app_context():
            response = self.e.post("/api/v1/user/verify/")
            self.assertEqual(response.status_code,status.HTTP_200_OK)
            self.assertNotEqual(response.data, None)
            logger.info("Verify Token")
    
    def test_user_register(self):
        with app.app_context():
            response = self.e.post('/api/v1/user/', data={
                'username': faker.name(),
                'email': faker.email(),
                'password': 'passwordaja'
            })
            self.assertEqual(response.status_code,status.HTTP_200_OK)
            self.assertNotEqual(response.data, None)
            logger.info("User Register")
