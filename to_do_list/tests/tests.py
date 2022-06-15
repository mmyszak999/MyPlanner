import json
from django.contrib.auth.models import User
from django.test import Client
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from to_do_list.models import List, Task


class TestLoginSetUp(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create(username='testuser', password='test_user')
        cls.super_user = User.objects.create(username="superuser", password="super_user")
        cls.super_user.is_superuser = True
        cls.super_user.save()
        
        cls.lists = List.objects.bulk_create([
            List(title="shopping_list", owner=cls.test_user),
            List(title="business_objectives", owner=cls.super_user),
            List(title="weekly_goals", owner=cls.test_user)
        ])

    
    def setUp(self):
        self.client.force_login(self.test_user)

    def test_create_list(self):
        self.user_data = {'title': 'my_list', 'owner': self.test_user.id}
        response = self.client.post(reverse('api:list-lists'), data=self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.user_data['title'], str(List.objects.get(id=4)))
        
    def test_get_all_lists(self):
        obj_count = List.objects.filter(owner=self.test_user).count()
        response = self.client.get(reverse('api:list-lists'))
        self.assertEqual((len(response.data)), obj_count)
    
    def test_get_single_list(self):
        self.obj = List.objects.get(id=3)
        response = self.client.get(reverse('api:list-single-list', kwargs={'pk': self.obj.pk}))
        self.assertEqual(response.data['id'], self.obj.pk)