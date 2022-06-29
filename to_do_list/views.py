from requests import request
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin
)
from django.shortcuts import get_object_or_404

from to_do_list.serializers import ListSerializer, TaskInputSerializer, TaskOutputSerializer
from to_do_list.models import List, Task

class ListView(GenericAPIView, ListModelMixin, CreateModelMixin):
    serializer_class = ListSerializer
    
    def get_queryset(self):
        qs = List.objects.all()
        if self.request.user.is_staff or self.request.user.is_superuser:
            return qs
        return qs.filter(owner=self.request.user.id)

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)

class ListDetailView(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    serializer_class = ListSerializer

    def get_object(self):
        pk = self.kwargs['pk']
        return get_object_or_404(List, pk=pk)

    def get(self, request, pk):
        return self.retrieve(request, pk)

    def put(self, request, pk):
        return self.update(request, pk)

    def delete(self, request, pk):
        return self.destroy(request, pk)

class TaskView(GenericAPIView, ListModelMixin, CreateModelMixin):
    serializer_class = [TaskOutputSerializer, TaskInputSerializer]
    model = Task 
    
    def get_queryset(self):
        tasks = Task.objects.all()
        if not (self.request.user.is_staff or self.request.user.is_superuser):
            tasks = tasks.filter(task_list__owner=self.request.user.id)
        if (search := self.request.query_params.get("task_list")) is not None:
            return tasks.filter(task_list=search)
        return tasks
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TaskOutputSerializer
        return TaskInputSerializer
            
    def get(self, request):
        return self.list(request)
    
    def post(self, request):
        return self.create(request)

class TaskDetailView(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    serializer_class = [TaskOutputSerializer, TaskInputSerializer]
    model = Task
    
    def get_queryset(self):
        tasks = Task.objects.all()
        if not (self.request.user.is_staff or self.request.user.is_superuser):
            tasks = tasks.filter(task_list__owner=self.request.user.id)
        if (search := self.request.query_params.get("task_list")) is not None:
            return tasks.filter(task_list=search)
        return tasks
    
    def get_object(self):
        return super().get_object()
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TaskOutputSerializer
        return TaskInputSerializer

    def get(self, request, pk):
        return self.retrieve(request, pk)
    
    def put(self, request, pk):
        return self.update(request, pk)

    def delete(self, request, pk):
        return self.destroy(request, pk)