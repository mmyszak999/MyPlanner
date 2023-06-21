from django.urls import reverse
from django.contrib.auth import get_user
from rest_framework import status

from api.tests.test_setup import TestSetUp
from api.models import Task


class TestTasks(TestSetUp):
    def test_create_task(self):
        list_id = self.lists[0].id
        self.task_data = {'body': '3 bottles of water', 'task_list': list_id, 'priority': 'B'}
        response = self.client.post(reverse('api:list-tasks-in-list', kwargs={'pk': list_id}), data=self.task_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.task_data['body'], Task.objects.get(task_list=list_id, body=self.task_data['body']).body)

    def test_get_all_tasks_from_the_list(self):
        list_ = self.lists[0]
        response = self.client.get(reverse('api:list-tasks-in-list', kwargs={'pk': list_.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual((len(response.data)), Task.objects.filter(task_list=list_.id).count())

    def test_get_single_task(self):
        self.obj = self.tasks[1]
        response = self.client.get(
            reverse('api:list-single-task-in-list', kwargs={'pk': self.obj.task_list.id, 'task_pk': self.obj.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.obj.pk)

    def test_update_single_task(self):
        self.obj = self.tasks[1]
        new_body = 'Updated List Title'
        response = self.client.put(reverse('api:list-single-task-in-list',
                                           kwargs={'pk': self.obj.task_list.id, 'task_pk': self.obj.pk}),
                                   data={'body': new_body, 'task_list': self.obj.task_list.id, 'priority': 'B'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['body'], new_body)

    def test_delete_single_task(self):
        self.obj = self.tasks[1]
        response = self.client.delete(
            reverse('api:list-single-task-in-list', kwargs={'pk': self.obj.task_list.id, 'task_pk': self.obj.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_task_with_the_nonexistent_list(self):
        list_id = 2137
        self.task_data = {'body': '3 bottles of water', 'task_list': list_id, 'priority': 'A'}
        response = self.client.post(reverse('api:list-tasks-in-list', kwargs={'pk': list_id}), data=self.task_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_task_with_an_incorrect_priority(self):
        priority = 'Z'
        self.task_data = {'body': '5 apples', 'task_list': self.lists[0].id, 'priority': priority}
        response = self.client.post(reverse('api:list-tasks-in-list', kwargs={'pk': self.lists[0].id}),
                                    data=self.task_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_if_test_user_can_not_get_all_tasks_from_not_their_list(self):
        self.client.force_login(self.test_user)
        tasks = Task.objects.filter(task_list=self.lists[1].id).count()
        response = self.client.get(reverse('api:list-tasks-in-list', kwargs={'pk': self.lists[1].id}))
        self.assertNotEqual(tasks, len(response.data))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_if_test_user_can_not_post_task_to_not_their_list(self):
        self.client.force_login(self.test_user)
        list_id = self.lists[1].id
        self.task_data = {'body': 'Sign the deal with an asian company', 'task_list': list_id, 'priority': 'C'}
        response = self.client.post(reverse('api:list-tasks-in-list', kwargs={'pk': list_id}), data=self.task_data)
        self.assertNotEqual(get_user(self.client), self.super_user)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
