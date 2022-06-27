from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin
)
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
        obj = List.objects.get(pk=pk)
        if(
            self.request.user.is_staff or 
            self.request.user.is_superuser or
            self.request.user == obj.owner):
            return get_object_or_404(List, pk=pk)
        raise PermissionDenied

    def get(self, request, pk):
        return self.retrieve(request, pk)

    def put(self, request, pk):
        return self.update(request, pk)

    def delete(self, request, pk):
        return self.destroy(request, pk)

class TasksInTheList(GenericAPIView, ListModelMixin):
    serializer_class = TaskSerializer
    model = Task

    def get_queryset(self):
        qs = Task.objects.filter(task_list=self.kwargs['pk'])
        if not qs.exists():
            raise NotFound
        list_owner_id = qs.values('task_list__owner')[0]['task_list__owner']
        if(
            self.request.user.is_staff or 
            self.request.user.is_superuser or
            self.request.user.id == list_owner_id):
            return qs
        raise PermissionDenied

    def get(self, request, pk):
        return self.list(request)

class TaskView(GenericAPIView, ListModelMixin, CreateModelMixin):
    serializer_class = TaskSerializer
    model = Task 
    
    def get_queryset(self):
        qs = Task.objects.all()
        if self.request.user.is_staff or self.request.user.is_superuser:
            return qs
        return qs.filter(task_list__owner=self.request.user)
            
    def get(self, request):
        return self.list(request)
    
    def post(self, request):
        return self.create(request)

class TaskDetailView(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    serializer_class = TaskSerializer
    model = Task
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['task_list'] = Task.task_list
        data['priority'] = Task.priority
        data['request'] = self.request
        return data
    
    def get_object(self):
        pk = self.kwargs['pk']
        return get_object_or_404(Task, pk=pk)

    def get(self, request, pk):
        return self.retrieve(request, pk)
    
    def put(self, request, pk):
        return self.update(request, pk)

    def delete(self, request, pk):
        return self.destroy(request, pk)