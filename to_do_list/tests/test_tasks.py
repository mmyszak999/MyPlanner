from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user

from .test_setup import TestSetUp
from to_do_list.models import Task

class TestTasks(TestSetUp):
    def test_create_task(self):
        self.task_data = {'body': '3 bottles of water', 'task_list': 1, 'priority': 'B'}
        response = self.client.post(reverse('api:task-tasks'), data=self.task_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.task_data['body'], str(Task.objects.get(id=self.task_count + 1)))
        self.assertEqual(response.request['PATH_INFO'], '/api/tasks/')
        
    def test_get_all_tasks(self):
        response = self.client.get(reverse('api:task-tasks'))
        self.assertEqual((len(response.data)), self.task_count)

    def test_get_single_task(self):
        self.obj = Task.objects.select_related('task_list').get(pk=self.task_pk)
        response = self.client.get(reverse('api:task-single-task', kwargs={'pk': self.obj.pk}))
        self.assertEqual(response.data['id'], self.obj.pk)
    
    def test_update_single_task(self):
        self.obj = Task.objects.select_related('task_list').get(pk=self.list_pk)
        new_body = 'Updated List Title'
        response = self.client.put(reverse('api:task-single-task', kwargs={'pk': self.obj.pk}), data=
        {'body': new_body, 'task_list': self.obj.task_list.id, 'priority': 'B'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['body'], new_body)
    
    def test_delete_single_list(self):
        self.obj = Task.objects.select_related('task_list').get(pk=self.task_pk)
        response = self.client.delete(reverse('api:task-single-task', kwargs={'pk': self.obj.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_tasks_from_the_list(self):
        pk_ = self.list_pk
        self.tasks_in_list_count = Task.objects.filter(task_list=pk_).select_related('task_list').count()
        response = self.client.get(reverse('api:task-tasks'), {'task_list': pk_})
        self.assertEqual(len(response.data), self.tasks_in_list_count)
        self.assertEqual(response.request['QUERY_STRING'], f"task_list={pk_}")
    
    def test_create_task_with_the_nonexistent_list(self):
        list_pk = 2137
        self.task_data = {'body': '3 bottles of water', 'task_list': list_pk, 'priority': 'A' }
        response = self.client.post(reverse('api:task-tasks'), data=self.task_data)
        error_message = response.data['task_list'][0]
        self.assertEqual(str(error_message), f'Invalid pk "{list_pk}" - object does not exist.')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_task_with_an_incorrect_priority(self):
        priority = 'Z'
        self.task_data = {'body': '5 apples', 'task_list': 1, 'priority': priority}
        response = self.client.post(reverse('api:task-tasks'), data=self.task_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['priority'][0], f'"{priority}" is not a valid choice.')