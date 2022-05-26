from rest_framework.generics import GenericAPIView

from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin
)
from rest_framework_simplejwt.authentication import JWTAuthentication

from to_do_list.serializers import ListSerializer, TaskSerializer
from to_do_list.models import List, Task
from to_do_list.permissions import MyOwnPermissions


class ListView(GenericAPIView, ListModelMixin, CreateModelMixin):
    queryset = List.objects.all()
    serializer_class = ListSerializer
    permission_classes = (MyOwnPermissions,)
    authentication_classes = (JWTAuthentication,)
    
    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return self.queryset
        return self.queryset.filter(owner=self.request.user)

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)

class ListDetailView(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    serializer_class = ListSerializer
    permission_classes = (MyOwnPermissions,)
    authentication_classes = (JWTAuthentication,)

    def get_object(self):
        pk = self.kwargs['pk']
        return List.objects.get(pk=pk)

    def get(self, request, pk):
        return self.retrieve(request, pk)

    def put(self, request, pk):
        return self.update(request, pk)

    def delete(self, request, pk):
        return self.destroy(request, pk)

class TaskView(GenericAPIView, ListModelMixin, CreateModelMixin):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (MyOwnPermissions,)
    authentication_classes = (JWTAuthentication,) 
    
    def get_queryset(self):
        search = self.request.query_params.get('task_list')
        tasks = self.queryset
        if not (self.request.user.is_staff or self.request.user.is_superuser):
            tasks = Task.objects.filter(task_list__owner=self.request.user)
        if (search := self.request.query_params.get("task_list")) is not None:
            return tasks.filter(task_list=search)
        return tasks
            
    def get(self, request):
        return self.list(request)
    
    def post(self, request):
        return self.create(request)

class TaskDetailView(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    serializer_class = TaskSerializer
    permission_classes = (MyOwnPermissions,)
    authentication_classes = (JWTAuthentication,)

    def get_object(self):
        pk = self.kwargs['pk']
        return Task.objects.get(pk=pk)

    def get(self, request, pk):
        return self.retrieve(request, pk)
    
    def put(self, request, pk):
        return self.update(request, pk)

    def delete(self, request, pk):
        return self.destroy(request, pk)