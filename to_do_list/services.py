from django.contrib.auth.models import User
from rest_framework.request import Request

from to_do_list.serializers import ListInputSerializer, TaskInputSerializer
from to_do_list.entities.service_entities import ListEntity, TaskEntity
from to_do_list.models import List, Task


class ListCreateService:

    def list_create(self, dto: ListEntity, user: User) -> List:
        return List.objects.create(
            title=dto.title,
            owner=user
        )

    @classmethod
    def _build_list_dto_from_request_data(cls, request_data) -> ListEntity:
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
    def _build_list_dto_from_request_data(cls, request_data, instance: List) -> ListEntity:
        serializer = ListInputSerializer(instance, data=request_data, partial=True)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        return ListEntity(
            title=data['title'],
        )

class TaskCreateService:
    
    def task_create(self, dto: TaskEntity, list_instance=List) -> Task:
        return Task.objects.create(
            body=dto.body,
            task_list=list_instance,
            priority=dto.priority
        )


    @classmethod
    def _build_list_dto_from_request_data(cls, request, pk: int) -> ListEntity:

        return ListEntity(
            title=request.data['title'],
        )

    @classmethod
    def _build_task_dto_from_request_data(cls, request, pk: int) -> TaskEntity:
        serializer = TaskInputSerializer(data=request.data, context={'request': request})
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
    def _get_list_instance(cls, pk: int) -> List:
        return List.objects.get(pk=pk)
    
    @classmethod
    def _build_list_dto_from_validated_data(cls, request: Request, pk: int) -> ListEntity:
        instance = cls._get_list_instance(pk)

        return ListEntity(
            title=instance.title
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
            priority=data['priority'],
        )

    
