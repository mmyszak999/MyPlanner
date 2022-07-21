import dacite.core as dacite
from dataclasses import dataclass

from django.contrib.auth.models import User
from requests import request
from rest_framework.request import Request
from rest_framework.response import Response

from to_do_list.serializers import ListInputSerializer, TaskInputSerializer
from to_do_list.entities.service_entities import ListEntity, TaskEntity
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
    def list_update(self, dto, pk: int) -> List:
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
    
    def task_create(self, dto, list_pk: int) -> Task:
        return Task.objects.create(
            body=dto.body,
            task_list=self._get_list_instance(list_pk),
            priority=dto.priority
        )
    
    @classmethod
    def _get_list_instance(cls, pk: int) -> List:
        return List.objects.get(pk=pk)


    @classmethod
    def _build_list_dto_from_validated_data(cls, request: Request, pk: int) -> ListEntity:
        instance = cls._get_list_instance(pk)

        return ListEntity(
            title=instance.title,
            owner=request.user
        )

    @classmethod
    def _build_task_dto_from_validated_data(cls, request: Request, pk: int) -> TaskEntity:
        serializer = TaskInputSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        return TaskEntity(
            body=data['body'],
            task_list=cls._build_list_dto_from_validated_data(request, pk),
            priority=data['priority'],
        )

class TaskUpdateService:
    def task_update(self, dto, task_pk: int, pk: int) -> Task:
        instance, if_created = Task.objects.filter(id=task_pk).update_or_create(
            task_list=self._get_list_instance(pk),
            defaults={'body': dto.body, 'priority': dto.priority}
        )
        return instance
    
    @classmethod
    def _get_list_instance(cls, pk: int) -> List:
        return List.objects.get(pk=pk)
    
    @classmethod
    def _build_list_dto_from_validated_data(cls, request: Request, pk: int) -> ListEntity:
        instance = cls._get_list_instance(pk)

        return ListEntity(
            title=instance.title,
            owner=request.user
        )

    @classmethod
    def _build_task_dto_from_validated_data(cls, request: Request, pk: int, instance: Task) -> TaskEntity:
        serializer = TaskInputSerializer(instance, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        instance.body = data['body']
        instance.priority = data['priority']
        instance.save()

        return TaskEntity(
            body=data['body'],
            task_list=cls._build_list_dto_from_validated_data(request, pk),
            priority=data['priority'],
        )

    
