import unittest
import random
from database.models.category import Category
from database.models.product import Product
from rest_framework import status
from rest_framework.test import APIClient
from django.core.files import File
import logging
from django.urls import reverse
from faker import Faker
from cashier_user.tests.user_tests import tokens, readme

faker = Faker()


class Producttests(unittest.TestCase):
    def setUp(self):
        self.e = APIClient()
        self.logger = logging.getLogger(__name__)

    def test_category(self):
        self.logger.critical("category tests")

    @unittest.skipIf(not tokens, "tokens is expires")
    def test_category_get_all(self):
        urls = reverse("all-category")
        self.e.credentials(HTTP_AUTHORIZATION="Bearer " + readme)
        response = self.e.get(urls, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.logger.info("get all category : %s" % response.data)

    @unittest.skipIf(Category.objects.count() == 0, "category not have data")
    @unittest.skipIf(not tokens, "tokens is expires")
    def test_category_get_detail(self):
        category = Category.objects.first()
        urls = reverse("category-detail", args=[category.id])
        self.e.credentials(HTTP_AUTHORIZATION="Bearer " + readme)
        response = self.e.get(urls, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.logger.info("get detail category")

    @unittest.skipIf(not tokens, "tokens is expires")
    def test_category_create(self):
        urls = reverse("category-list")
        self.e.credentials(HTTP_AUTHORIZATION="Bearer " + readme)
        data = {
            "name": faker.name(),
            "author": tokens.get("user").accounts_set.first().id,
        }
        response = self.e.post(urls, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "Category has been created")
        self.logger.info("create category")

    @unittest.skipIf(Category.objects.count() == 0, "category not have data")
    @unittest.skipIf(not tokens, "tokens is expires")
    def test_category_destroy(self):
        category = Category.objects.first()
        urls = reverse("category-detail", args=[category.public_id])
        self.e.credentials(HTTP_AUTHORIZATION="Bearer " + readme)
        response = self.e.delete(urls, format="json")
        self.assertEqual(response.data["message"], "Category has been deleted")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.logger.info("category has been destroy")

    @unittest.skipIf(Category.objects.count() == 0, "category not have data")
    @unittest.skipIf(not tokens, "tokens is expires")
    def test_category_updated(self):
        category = Category.objects.first()
        urls = reverse("category-detail", args=[category.public_id])
        self.e.credentials(HTTP_AUTHORIZATION="Bearer " + readme)
        data = {"name": faker.name()}
        response = self.e.put(urls, data, format="json")
        self.assertEqual(response.data["message"], "Category has been updated")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.logger.info("category has been updated")

    def test_product(self):
        self.logger.critical("product tests")

    @unittest.skipIf(Product.objects.count() == 0, "category not have data")
    @unittest.skipIf(not tokens, "tokens is expires")
    def test_product_get_all(self):
        urls = reverse("all-product")
        self.e.credentials(HTTP_AUTHORIZATION="Bearer " + readme)
        response = self.e.get(urls, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.logger.info("get all product : %s" % response.data)

    @unittest.skipIf(Product.objects.count() == 0, "category not have data")
    @unittest.skipIf(not tokens, "tokens is expires")
    def test_product_get_detail(self):
        product = Product.objects.first()
        urls = reverse("product-detail", args=[product.id])
        self.e.credentials(HTTP_AUTHORIZATION="Bearer " + readme)
        response = self.e.get(urls, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.logger.info("get detail product")

    @unittest.skipIf(Category.objects.count() == 0, "category not have data")
    @unittest.skipIf(not tokens, "tokens is expires")
    def test_product_create(self):
        category = Category.objects.first()
        urls = reverse("product-list")
        self.e.credentials(HTTP_AUTHORIZATION="Bearer " + readme)
        description = ""
        for i in faker.paragraphs():
            description += i
        _ = []
        for i in range(1,5):
            _dict = {}
            _dict['child'] = faker.color()
            _.append(_dict)
        data = {
            "name": faker.name(),
            "description": description,
            "category": category.id,
            "author": tokens.get("user").accounts_set.first().id,
            "stock": random.randint(10, 20),
            "max_stock": random.randint(30, 40),
            "type": faker.name(),
            'hex': _,
            "price": random.randint(10000, 90000),
            "sell": random.randint(20000, 90000),
            "icons": File(open("IMG_0083.PNG", "rb")),
        }
        response = self.e.post(urls, data, format="multipart")
        self.assertEqual(response.data["message"], "Product has been created")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.logger.info("product has been created")

    @unittest.skipIf(not tokens, "tokens is expires")
    @unittest.skipIf(Product.objects.count() == 0, "product not have data")
    def test_product_destory(self):
        product = Product.objects.first()
        urls = reverse("product-detail", args=[product.public_id])
        self.e.credentials(HTTP_AUTHORIZATION="Bearer " + readme)
        response = self.e.delete(urls, format="json")
        self.assertEqual(response.data["message"], "Product has been deleted")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.logger.info("product has been deleted")

    @unittest.skipIf(not tokens, "tokens is expires")
    @unittest.skipIf(Product.objects.count() == 0, "product not have data")
    def test_product_update(self):
        product = Product.objects.first()
        urls = reverse("updated-product", args=[product.public_id])
        self.e.credentials(HTTP_AUTHORIZATION="Bearer " + readme)
        description = ""
        for i in faker.paragraphs():
            description += i
        data = {
            "name": faker.name(),
            "description": description,
            "author": tokens.get("user").accounts_set.first().id,
            "stock": random.randint(10, 20),
            "max_stock": random.randint(30, 40),
            "type": faker.name(),
            "price": random.randint(10000, 90000),
            "sell": random.randint(20000, 90000),
            "icons": File(open("IMG_0083.PNG", "rb")),
            "typeId": product.type.all().first().id,
        }
        response = self.e.post(urls, data, format="multipart")
        print(response.data)
        self.assertEqual(response.data["message"], "Product has been updated")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.logger.info("product has been updated")
