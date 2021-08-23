import unittest
import faker
from flask_api import status
from faker import Faker
from api_server.server import create_app
from core.logger import logger
import json

faker = Faker()

app = create_app()
exists = None

with app.app_context():
    from api_database.user import User
    exists = User.query.count()

with open("token.txt", "r") as r:
    readme = r.read()

with open("x-token-api.txt", "r") as r:
    readmes = r.read()

class UserTests(unittest.TestCase):
    def setUp(self):
        self.e = None
        with app.test_client() as client:
            self.e = client

    def test_user(self):
        logger.critical("UserTests")

    def test_user_register(self):
        with app.app_context():
            response = self.e.post('/api/v1/user/', data={
                'username': faker.name(),
                'email': faker.email(),
                'password': 'passwordaja'
            })
            self.assertEqual(response.status_code,status.HTTP_201_CREATED)
            self.assertNotEqual(response.data, None)
            logger.info("Create Accounts")


    @unittest.skipIf(not exists, "user not have data")
    def test_user_login(self):
        with app.app_context():
            response = self.e.post('/api/v1/user/login/', data={
                'username': User.query.first().username,
                'password': 'passwordaja'
            })
            self.assertEqual(response.status_code,status.HTTP_200_OK)
            self.assertNotEqual(response.data, None)
            logger.info("Generate Token")
            data = json.loads(response.data)
            with open("token.txt", "w") as w:
                w.write(data.get('token'))
            with open("x-token-api.txt", "w") as w:
                w.write(str(data.get('x-token-api')))

    @unittest.skipIf(not readme or not readmes, "token is expires")
    def test_user_verify_token(self):
        with app.app_context():
            response = self.e.post('/api/v1/user/verify/', headers={
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + readme,
                'x-token-api': 'Bearer ' + readmes
            })
            self.assertEqual(response.status_code,status.HTTP_200_OK)
            self.assertNotEqual(response.data, None)
            logger.info("Verify Token")

