from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin
)
from django.shortcuts import get_object_or_404

from to_do_list.serializers import ListInputSerializer, ListOutputSerializer, TaskInputSerializer, TaskOutputSerializer
from to_do_list.models import List, Task

class ListView(GenericAPIView, ListModelMixin, CreateModelMixin):
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

    def post(self, request: Request) -> Response:
        return self.create(request)

class ListDetailView(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
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

    def put(self, request: Request, pk: int) -> Response:
        return self.update(request, pk)

    def delete(self, request: Request, pk: int) -> Response:
        return self.destroy(request, pk)


class TasksInTheListView(GenericAPIView, ListModelMixin, CreateModelMixin):
    serializer_class = TaskOutputSerializer
    model = Task

    def get_queryset(self):
        qs = Task.objects.filter(task_list=self.kwargs['pk']).select_related('task_list')
        list_owner_id = List.objects.filter(id=self.kwargs['pk']).values('owner')[0]['owner']
        if (self.request.user.is_superuser
        or self.request.user.id == list_owner_id
        or not qs.exists()):
            return qs
        raise PermissionDenied

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TaskOutputSerializer
        return TaskInputSerializer
            
    def get(self, request: Request, pk: int) -> Response:
        return self.list(request)
    
    def post(self, request: Request, pk: int) -> Response:
        return self.create(request)

class TasksInTheListDetailView(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    serializer_class = TaskOutputSerializer
    model = Task
    
    def get_object(self):
        pk = self.kwargs['task_pk']
        list_id = self.kwargs['pk']
        obj = Task.objects.get(pk=pk)
        tasks = Task.objects.filter(task_list=list_id).select_related('task_list')
        if obj not in tasks:
            raise NotFound
        if self.request.user.is_superuser:
            return obj
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