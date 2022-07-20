import dacite.core as dacite
from dataclasses import dataclass

from django.contrib.auth.models import User
from requests import request
from rest_framework.request import Request
from rest_framework.response import Response

from to_do_list.serializers import ListInputSerializer
from to_do_list.entities.service_entities import ListEntity, UserEntity, TaskEntity
from to_do_list.models import List, Task


class ListCreateService:

    def list_create(self, dto) -> List:
        return List.objects.create(
            title=dto.title,
            owner=dto.owner
        )

    @classmethod
    def _build_list_dto_from_validated_data(cls, request: Request) -> ListEntity:
        serializer = ListInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        return ListEntity(
            title=data['title'],
            owner=request.user
        )

class ListUpdateService:
    def list_update(self, dto, pk: int):
        instance, if_created = List.objects.filter(id=pk).update_or_create(
            owner=dto.owner,
            defaults={'title': dto.title}
        )
        return instance

    @classmethod
    def _build_list_dto_from_validated_data(cls, request: Request, instance: List) -> ListEntity:
        serializer = ListInputSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        instance.title = data['title']
        instance.save()

        return ListEntity(
            title=data['title'],
            owner=request.user
        )

class TaskCreateService:
    
    def task_create(self):
        pass
    
    @classmethod
    def get_list_instance(cls):
        pass

    @classmethod
    def _build_task_dto_from_validated_data(cls):
        pass

