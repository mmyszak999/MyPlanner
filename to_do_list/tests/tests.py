from random import randint

from django.contrib.auth.models import User
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

        cls.lists = Task.objects.bulk_create([
            Task(body="milk", task_list=cls.lists[0], priority='C'),
            Task(body="lemon", task_list=cls.lists[0], priority='E'),
            Task(body="bread", task_list=cls.lists[0], priority='B'),

            Task(body="double the overall income in 2 years", task_list=cls.lists[1], priority='A'),
            Task(body="expand business to 3 continents", task_list=cls.lists[1], priority='D'),

            Task(body="do the training 3 times", task_list=cls.lists[2], priority='B'),
            Task(body="repair the chair", task_list=cls.lists[2], priority='D'),
            Task(body="buy new shoes", task_list=cls.lists[2], priority='E'),
        ])

        cls.list_count = List.objects.all().count()
        cls.task_count = Task.objects.all().count()

        cls.list_pk = randint(1, cls.list_count)
        cls.task_pk = randint(1, cls.task_count)

    def setUp(self):
        self.client.force_login(self.super_user)

    def test_create_list(self):
        self.user_data = {'title': 'my_list', 'owner': self.test_user.id}
        response = self.client.post(reverse('api:list-lists'), data=self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.user_data['title'], str(List.objects.get(id=4)))
        
    def test_get_all_lists(self):
        response = self.client.get(reverse('api:list-lists'))
        self.assertEqual((len(response.data)), self.list_count)
    
    def test_get_single_list(self):
        self.obj = List.objects.get(pk=self.list_pk)
        response = self.client.get(reverse('api:list-single-list', kwargs={'pk': self.obj.pk}))
        self.assertEqual(response.data['id'], self.obj.pk)

    def test_get_all_tasks(self):
        response = self.client.get(reverse('api:task-tasks'))
        self.assertEqual((len(response.data)), self.task_count)

    def test_get_single_task(self):
        self.obj = Task.objects.get(pk=self.task_pk)
        response = self.client.get(reverse('api:task-single-task', kwargs={'pk': self.obj.pk}))
        self.assertEqual(response.data['id'], self.obj.pk)
