import requests

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_503_SERVICE_UNAVAILABLE
from django.urls import reverse

from to_do_list.serializers import ListInputSerializer
from to_do_list.entities import entities
from to_do_list.models import List, Task

class ListCreateService:
    def list(self, dto):
        payload = self._prepare_payload(dto)

        try:
            response = requests.post(reverse('api:list-lists'), json=payload)
            response.raise_for_status()
        
        except requests.RequestException:
            return HTTP_503_SERVICE_UNAVAILABLE
        
        return List.objects.create(
            title=dto.title,
            owner=dto.owner
        )
    

    @staticmethod
    def _prepare_payload(dto):
        return {
            'title': dto.title,
            'owner': dto.owner
        }

