from random import randint

from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from to_do_list.models import List, Task


class TestSetUp(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create(username='testuser')
        cls.super_user = User.objects.create_superuser(username="superuser")
        
        cls.lists = List.objects.bulk_create([
            List(title="shopping_list", owner=cls.test_user),
            List(title="business_objectives", owner=cls.super_user),
            List(title="weekly_goals", owner=cls.test_user)
        ])

        cls.tasks = Task.objects.bulk_create([
            Task(body="milk", task_list=cls.lists[0], priority='C'),
            Task(body="lemon", task_list=cls.lists[0], priority='E'),
            Task(body="bread", task_list=cls.lists[0], priority='B'),

            Task(body="double the overall income in 2 years", task_list=cls.lists[1], priority='A'),
            Task(body="expand business to 3 continents", task_list=cls.lists[1], priority='D'),

            Task(body="do the training 3 times", task_list=cls.lists[2], priority='B'),
            Task(body="repair the chair", task_list=cls.lists[2], priority='D'),
            Task(body="buy new shoes", task_list=cls.lists[2], priority='E'),
        ])

        cls.list_count = List.objects.count()
        cls.task_count = Task.objects.count()

        cls.list_pk = randint(1, cls.list_count)
        cls.task_pk = randint(1, cls.task_count)

    def setUp(self):
        self.client.force_login(self.super_user)