from typing import OrderedDict
from django.contrib.auth.models import User

from api.serializers import ListInputSerializer, TaskInputSerializer
from api.entities.service_entities import ListEntity, TaskEntity
from api.models import List, Task


class ListCreateService:

    def list_create(self, dto: ListEntity, user: User) -> List:
        return List.objects.create(
            title=dto.title,
            owner=user
        )

    @classmethod
    def _build_list_dto_from_request_data(cls, request_data: OrderedDict) -> ListEntity:
        serializer = ListInputSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        return ListEntity(
            title=data['title']
        )


class ListUpdateService:
    def list_update(self, dto: ListEntity, instance: List) -> List:
        instance.title = dto.title
        instance.save(update_fields=['title'])

        return instance

    @classmethod
    def _build_list_dto_from_request_data(cls, request_data: OrderedDict, instance: List) -> ListEntity:
        serializer = ListInputSerializer(instance, data=request_data, partial=True)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        return ListEntity(
            title=data['title'],
        )


class TaskCreateService:

    def task_create(self, dto: TaskEntity, list_instance: List) -> Task:
        return Task.objects.create(
            body=dto.body,
            task_list=list_instance,
            priority=dto.priority
        )

    @classmethod
    def _build_task_dto_from_request_data(cls, request_data: OrderedDict) -> TaskEntity:
        serializer = TaskInputSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        return TaskEntity(
            body=data['body'],
            priority=data['priority'],
        )


class TaskUpdateService:
    def task_update(self, dto: TaskEntity, instance: Task) -> Task:
        instance.body = dto.body
        instance.priority = dto.priority
        instance.save(update_fields=['body', 'priority'])

        return instance

    @classmethod
    def _build_task_dto_from_validated_data(cls, request_data: OrderedDict, instance: Task) -> TaskEntity:
        serializer = TaskInputSerializer(instance, data=request_data, partial=True)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        return TaskEntity(
            body=data['body'],
            priority=data['priority'],
        )
