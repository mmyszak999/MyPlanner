import json

from rest_framework import status

from to_do_list.models import List
from to_do_list.serializers import ListSerializer
from .test_setup import TestSetUp

class TestListModel(TestSetUp):
    def test_create_list(self):
        response = self.client.post("http://127.0.0.1:8000/api/lists/", self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
