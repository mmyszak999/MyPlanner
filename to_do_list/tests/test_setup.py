from django.contrib.auth.models import User
from rest_framework.test import APITestCase


class TestSetUp(APITestCase):

    def setUp(self):
        self.user_obj = User.objects.create_user("test_user",'',"test_user")
        self.user_data = {"title": "test_list", 'owner': self.user_obj.id}
        return super().setUp()


        
