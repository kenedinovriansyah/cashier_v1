import unittest
from database.models.category import Category
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

    @unittest.skipIf(not tokens, 'tokens is expires')
    def test_category_create(self):
        urls = reverse('category-list')
        self.e.credentials(HTTP_AUTHORIZATION="Bearer " + readme)
        data = {
            'name': faker.name(),
            'author': tokens.get('user').accounts_set.first().id
        }
        response = self.e.post(urls,data,format='multipart')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Category has been created')
        self.logger.info('create category')

    @unittest.skipIf(Category.objects.count() == 0, 'category not have data')
    @unittest.skipIf(not tokens, 'tokens is expires')
    def test_category_destroy(self):
        category = Category.objects.first()
        urls = reverse('category-detail', args=[category.public_id])
        self.e.credentials(HTTP_AUTHORIZATION="Bearer " + readme)
        response = self.e.delete(urls,format='json')
        self.assertEqual(response.data['message'], 'Category has been deleted')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.logger.info('category has been destroy')

    @unittest.skipIf(Category.objects.count() == 0, 'category not have data')
    @unittest.skipIf(not tokens, 'tokens is expires')
    def test_category_updated(self):
        category = Category.objects.first()
        urls = reverse('category-detail', args=[category.public_id])
        self.e.credentials(HTTP_AUTHORIZATION="Bearer " + readme)
        data = {
            'name': faker.name()
        }
        response = self.e.put(urls,data,format='json')
        self.assertEqual(response.data['message'], 'Category has been updated')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.logger.info('category has been updated')
    