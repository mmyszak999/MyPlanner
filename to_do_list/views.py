from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from to_do_list.serializers import ListSerializer, TaskSerializer
from to_do_list.models import List, Task

class ListView(GenericAPIView, ListModelMixin, CreateModelMixin):
    serializer_class = ListSerializer
    
    def get_queryset(self):
        qs = List.objects.all()
        if self.request.user.is_staff or self.request.user.is_superuser:
            return qs
        return qs.filter(owner=self.request.user)

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
    serializer_class = TaskSerializer 
    
    def get_queryset(self):
        search = self.request.query_params.get('task_list')
        tasks = Task.objects.all()
        if not (self.request.user.is_staff or self.request.user.is_superuser):
            tasks = tasks.filter(task_list__owner=self.request.user)
        if (search := self.request.query_params.get("task_list")) is not None:
            return tasks.filter(task_list=search)
        return tasks
            
    def get(self, request):
        return self.list(request)
    
    def post(self, request):
        return self.create(request)

class TaskDetailView(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    serializer_class = TaskSerializer

    def get_object(self):
        pk = self.kwargs['pk']
        single_task = get_object_or_404(Task, pk=pk)
        if (self.request.user == single_task.task_list.owner or
            self.request.user.is_staff or self.request.user.is_superuser):
            return single_task
        raise PermissionDenied({"message": "You don't have permission to access"})

    def get(self, request, pk):
        return self.retrieve(request, pk)
    
    def put(self, request, pk):
        return self.update(request, pk)

    def delete(self, request, pk):
        return self.destroy(request, pk)