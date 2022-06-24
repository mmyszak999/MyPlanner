from django.urls import reverse

from .test_setup import TestSetUp
from to_do_list.models import List, Task
from django.contrib.auth import get_user


class TestUser(TestSetUp):
    def setUp(self):
        self.client.logout()
        self.client.force_login(self.test_user)

    def test_if_user_logged_in(self):
        current_user = get_user(self.client)
        self.assertTrue(current_user.is_authenticated)
    
    def test_if_test_user_can_get_all_lists(self):
        lists = List.objects.all().count()
        response = self.client.get(reverse('api:list-lists'))
        self.assertNotEqual(lists, len(response.data))

    def test_if_test_user_can_get_all_tasks(self):
        tasks = Task.objects.all().count()
        response = self.client.get(reverse('api:task-tasks'))
        self.assertNotEqual(tasks, len(response.data))
    
    def test_if_test_user_can_post_task_to_not_their_list(self):
        task_pk = 2
        self.task_data = {'body': 'Sign the deal with an asian company', 'task_list': task_pk, 'priority': 'C' }
        response = self.client.post(reverse('api:task-tasks'), data=self.task_data)
        self.assertEqual(response.data['non_field_errors'][0], "You are not the list owner")