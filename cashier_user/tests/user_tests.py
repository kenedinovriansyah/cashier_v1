from database.models.accounts import choice
from faker import Faker
from rest_framework import status
from rest_framework.test import APIClient
from django.core.files import File
from django.urls import reverse
import unittest
import logging
from django.contrib.auth.models import User
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer

faker = Faker(["id_ID"])

with open("token.txt", "r") as r:
    readme = r.read()

tokens = None
try:
    tokens = VerifyJSONWebTokenSerializer().validate({"token": readme})
except:
    tokens = None


class Usertests(unittest.TestCase):
    def setUp(self):
        self.e = APIClient()
        self.logger = logging.getLogger(__name__)

    def test_user(self):
        self.logger.critical("usertests")

    @unittest.skipIf(User.objects.count() == 0, "user not have data")
    def test_user_login(self):
        urls = reverse("authtoken")
        user = User.objects.first()
        data = {"username": user.username, "password": "Password@123"}
        response = self.e.post(urls, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data["token"], None)
        self.logger.info("user login")
        with open("token.txt", "w") as w:
            w.write(response.data["token"])

    @unittest.skipIf(not tokens, "tokens is expires")
    def test_user_refresh_token(self):
        urls = reverse("refresh-authtoken")
        data = {"token": readme}
        response = self.e.post(urls, data, format="json")
        self.assertNotEqual(response.data["token"], None)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.logger.info("refresh token")

    @unittest.skipIf(not tokens, "token is expires")
    def test_user_verify_token(self):
        urls = reverse("verify-authtoken")
        data = {"token": readme}
        response = self.e.post(urls, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data["token"], None)
        self.logger.info("verify token")

    def test_user_create(self):
        urls = reverse("user-list")
        data = {
            "username": faker.user_name(),
            "email": faker.email(),
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "password": "Password@123",
            "password_confirmation": "Password@123",
        }
        response = self.e.post(urls, data, format="json")
        self.assertEqual(response.data["message"], "Accounts has been created")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.logger.info("create user")

    @unittest.skipIf(User.objects.count() == 0, "user not have data")
    def test_user_reset(self):
        urls = reverse("user-list")
        user = User.objects.first()
        data = {"token": user.username, "types": "reset"}
        response = self.e.post(urls, data, format="json")
        self.assertEqual(
            response.data["message"],
            "Account has been reset, please check your email inbox for a new password sandi",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.logger.info("reset user")

    @unittest.skipIf(not tokens, "tokens is expires")
    def test_user_zupdated(self):
        urls = reverse("updated-accounts")
        self.e.credentials(HTTP_AUTHORIZATION="Bearer " + readme)
        data = {
            "username": faker.user_name(),
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "gender": choice.male,
            "country": faker.country(),
            "state": faker.state(),
            "address": faker.address(),
            "postal_code": faker.postcode(),
            "phone": faker.phone_number(),
            "phone_fax": faker.phone_number(),
            "type": choice.owner,
        }
        response = self.e.post(urls, data, format="json")
        self.assertEqual(response.data["message"], "Profile has been updated")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.logger.info("update profile")

    @unittest.skipIf(not tokens, "tokens is expiress")
    def test_user_updated_email(self):
        urls = reverse("updated-accounts")
        self.e.credentials(HTTP_AUTHORIZATION="Bearer " + readme)
        data = {"email": faker.email(), "password": "Password@123", "types": "email"}
        response = self.e.post(urls, data, format="json")
        self.assertEqual(response.data["message"], "Email has been updated")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.logger.info("updated email")

    @unittest.skipIf(not tokens, "tokens is expires")
    def test_user_updated_password(self):
        urls = reverse("updated-accounts")
        self.e.credentials(HTTP_AUTHORIZATION="Bearer " + readme)
        data = {
            "old_password": "Password@123",
            "password": "Password@123",
            "password_confirmation": "Password@123",
            "types": "password",
        }
        response = self.e.post(urls, data, format="json")
        self.assertEqual(response.data["message"], "Password has been updated")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.logger.info("updated password")

    @unittest.skipIf(not tokens, "tokens is expires")
    def test_user_add_employe(self):
        urls = reverse("updated-accounts")
        self.e.credentials(HTTP_AUTHORIZATION="Bearer " + readme)
        data = {
            "avatar": File(open("IMG_0083.PNG", "rb")),
            "username": faker.user_name(),
            "email": faker.email(),
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "gender": choice.male,
            "country": faker.country(),
            "state": faker.state(),
            "address": faker.address(),
            "postal_code": faker.postcode(),
            "type": choice.owner,
            "types": "employe",
        }
        response = self.e.post(urls, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Employe has been add")
        self.logger.info("add employe")

    @unittest.skipIf(not tokens, "tokens is expires")
    def test_user_me(self):
        urls = reverse("me")
        self.e.credentials(HTTP_AUTHORIZATION="Bearer " + readme)
        response = self.e.get(urls, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.logger.info("user me")

    @unittest.skipIf(not tokens, "tokens is expires")
    def test_user_destroy(self):
        get = tokens.get("user").accounts_set.first().employe.first()
        self.e.credentials(HTTP_AUTHORIZATION="Bearer " + readme)
        urls = reverse("user-detail", args=[get.accounts_set.first().public_id])
        response = self.e.delete(urls, format="json")
        self.assertEqual(response.data["message"], "Employe has been deleted")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.logger.info("destroy accounts")

    @unittest.skipIf(not tokens, "tokens is expires")
    def test_user_updated_employe(self):
        user = tokens.get("user").accounts_set.first().employe.all().first()
        if user:
            urls = reverse(
                "updated-employe", args=[user.accounts_set.first().public_id]
            )
            self.e.credentials(HTTP_AUTHORIZATION="Bearer " + readme)
            data = {
                "username": faker.user_name(),
                "email": faker.email(),
                "first_name": faker.first_name(),
                "last_name": faker.last_name(),
                "gender": choice.male,
                "country": faker.country(),
                "state": faker.state(),
                "address": faker.address(),
                "postal_code": faker.postcode(),
                "phone": faker.phone_number(),
                "phone_fax": faker.phone_number(),
            }
            response = self.e.post(urls, data, format="multipart")
            self.assertEqual(response.data["message"], "Accounts has been updated")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.logger.info("updated employe")
