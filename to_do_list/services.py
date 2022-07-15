from sqlite3 import adapters
from attr import dataclass
import requests

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_503_SERVICE_UNAVAILABLE
from django.urls import reverse
from django.http import HttpResponse

from to_do_list.serializers import ListInputSerializer
from to_do_list.entities.service_entities import ListEntity
from to_do_list.models import List, Task

class ListCreateService:

    def list_create(self, dto) -> None:
        return (List.objects.create(
            title=dto.title,
            owner=dto.owner
        ))
                  
    @staticmethod
    def _prepare_payload(dto):
        return {
            'title': dto.title,
            'owner': dto.owner
        }
    
    def _build_list_dto_from_validated_data(self, request: Request) -> ListEntity:
        serializer = ListInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        return ListEntity(
            title=data['title'],
            owner=request.user
        )

