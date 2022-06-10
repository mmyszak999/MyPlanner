from django.contrib.auth.models import User
from django.test import Client
from rest_framework.test import APITestCase


class TestLoginSetUp(APITestCase):
    def setUp(self):
        self.c = Client()
        self.test_user = User.objects.create_user(username='testuser', password="test_user")
        self.super_user = User.objects.create_superuser(username="superuser", password="super_user")
        
        return super().setUp()