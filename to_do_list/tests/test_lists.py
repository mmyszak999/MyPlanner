from django.urls import reverse
from rest_framework import status

from to_do_list.tests.test_setup import TestSetUp
from to_do_list.models import List

class TestLists(TestSetUp):
    def test_create_list(self):
        self.user_data = {'title': 'my_list', 'owner': self.super_user.id}
        response = self.client.post(reverse('api:list-lists'), data=self.user_data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.user_data['title'], str(List.objects.filter(owner=self.super_user).latest('title')))
        
    def test_get_all_lists(self):
        response = self.client.get(reverse('api:list-lists'))
        self.assertEqual((len(response.data)), self.list_count)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_single_list(self):
        self.obj = List.objects.get(pk=self.list_pk)
        response = self.client.get(reverse('api:list-single-list', kwargs={'pk': self.obj.pk}))
        self.assertEqual(response.data['id'], self.obj.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_update_single_list(self):
        self.obj = List.objects.get(pk=self.list_pk)
        new_title = 'Updated Content'
        response = self.client.put(reverse('api:list-single-list', kwargs={'pk': self.obj.pk}), data={
            'title': new_title,
            'owner': self.super_user.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], new_title)
    
    def test_delete_single_list(self):
        self.obj = List.objects.get(pk=self.list_pk)
        response = self.client.delete(reverse('api:list-single-list', kwargs={'pk': self.obj.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_if_test_user_can_get_all_lists(self):
        self.client.force_login(self.test_user)
        lists = List.objects.all().count()
        response = self.client.get(reverse('api:list-lists'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(lists, len(response.data))
