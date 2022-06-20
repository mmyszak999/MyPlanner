from django.urls import reverse
from rest_framework import status

from .test_setup import TestSetUp
from to_do_list.models import List

class TestLists(TestSetUp):
    def test_create_list(self):
        self.user_data = {'title': 'my_list', 'owner': self.test_user.id}
        response = self.client.post(reverse('api:list-lists'), data=self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.user_data['title'], str(List.objects.get(id=self.list_count + 1)))
        self.assertEqual(response.request['PATH_INFO'], '/api/lists/')
        
    def test_get_all_lists(self):
        response = self.client.get(reverse('api:list-lists'))
        self.assertEqual((len(response.data)), self.list_count)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_single_list(self):
        self.obj = List.objects.get(pk=self.list_pk)
        response = self.client.get(reverse('api:list-single-list', kwargs={'pk': self.obj.pk}))
        self.assertEqual(response.data['id'], self.obj.pk)
