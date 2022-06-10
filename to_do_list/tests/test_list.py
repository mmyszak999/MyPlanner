from http import client
import json
from django.test import Client

from rest_framework import status

from to_do_list.models import List
from to_do_list.serializers import ListSerializer
from .setup_login import TestLoginSetUp
from django.urls import reverse


class TestListModel(TestLoginSetUp):
    def test_create_list(self):
        self.user_data = {'title': 'my_list', 'owner': self.test_user.id}
        self.response = self.client.post(reverse('api:list-lists'), data=self.user_data)
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        