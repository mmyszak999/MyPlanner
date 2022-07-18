from venv import create
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
)
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin
)
from django.shortcuts import get_object_or_404

from to_do_list.serializers import (
    ListInputSerializer, ListOutputSerializer,
    TaskInputSerializer, TaskOutputSerializer)
from to_do_list.models import List, Task
from to_do_list.services import ListCreateService, ListUpdateService


class ListView(GenericViewSet, ListModelMixin):
    serializer_class = ListOutputSerializer
    
    def get_queryset(self):
        qs = List.objects.all()
        if self.request.user.is_staff or self.request.user.is_superuser:
            return qs
        return qs.filter(owner=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ListOutputSerializer
        return ListInputSerializer

    def get(self, request: Request) -> Response:
        return self.list(request)
    
    def create(self, request: Request) -> Response:
        list_create_service = ListCreateService()
        dto = list_create_service._build_list_dto_from_validated_data(request)
        created_list = list_create_service.list_create(dto)
            
        return Response(self.serializer_class(created_list).data, status=HTTP_201_CREATED)

class ListDetailView(GenericViewSet, RetrieveModelMixin, DestroyModelMixin):
    serializer_class = ListOutputSerializer

    def get_object(self):
        pk = self.kwargs['pk']
        obj = List.objects.get(pk=pk)
        if(
            self.request.user.is_staff or 
            self.request.user.is_superuser or
            self.request.user == obj.owner):
            return get_object_or_404(List, pk=pk)
        raise PermissionDenied

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ListOutputSerializer
        return ListInputSerializer

    def get(self, request: Request, pk: int) -> Response:
        return self.retrieve(request, pk)

    def update(self, request: Request, pk: int) -> Response:
        list_instance = self.get_object()
        list_update_service = ListUpdateService()
        dto = list_update_service._build_list_dto_from_validated_data(request, list_instance)
        updated_list = list_update_service.list_update(dto, pk)
        print(self.serializer_class(updated_list))

        return Response(self.get_serializer(updated_list).data)
        
    def delete(self, request: Request, pk: int) -> Response:
        return self.destroy(request, pk)


class TaskView(GenericAPIView, ListModelMixin, CreateModelMixin):
    serializer_class = TaskOutputSerializer
    model = Task
    

    def get_queryset(self):
        tasks = Task.objects.filter(task_list=self.kwargs["pk"]).select_related("task_list")
        user = self.request.user
        if not (user.is_staff or user.is_superuser):
            raise PermissionDenied
        return tasks

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TaskOutputSerializer
        return TaskInputSerializer
            
    def get(self, request: Request, pk: int) -> Response:
        return self.list(request)
    
    def post(self, request: Request, pk: int) -> Response:
        return self.create(request)

class TaskDetailView(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    serializer_class = TaskOutputSerializer
    model = Task
    
    def get_object(self):
        pk = self.kwargs['task_pk']
        list_id = self.kwargs['pk']
        tasks = Task.objects.filter(task_list=list_id).select_related('task_list')
        if self.request.user.is_superuser:
            return get_object_or_404(tasks, pk=pk)
        return get_object_or_404(Task, pk=pk, task_list__owner=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TaskOutputSerializer
        return TaskInputSerializer

    def get(self, request: Request, pk: int, task_pk: int) -> Response:
        return self.retrieve(request, pk)
    
    def put(self, request: Request, pk: int, task_pk: int) -> Response:
        return self.update(request, pk)

    def delete(self, request: Request, pk: int, task_pk: int) -> Response:
        return self.destroy(request, pk)