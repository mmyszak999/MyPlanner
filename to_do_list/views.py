from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT
)
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin
)
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication

from to_do_list.serializers import ListSerializer, TaskSerializer
from to_do_list.models import List, Task
from to_do_list.permissions import MyOwnPermissions


class ListView(GenericAPIView, ListModelMixin, CreateModelMixin):
    serializer_class = ListSerializer
    permission_classes = (MyOwnPermissions,)
    authentication_classes = (JWTAuthentication,)
    
    def get_queryset(self, request):
        if request.user.is_staff or request.user.is_superuser:
            return get_list_or_404(List)
        return get_list_or_404(List, owner=request.user)

    def get(self, request):
        serializer = ListSerializer(self.get_queryset(request), many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def post(self, request):
        return CreateModelMixin.create(self, request)

class ListDetailView(GenericAPIView, UpdateModelMixin, DestroyModelMixin):
    serializer_class = ListSerializer
    permission_classes = (MyOwnPermissions,)
    authentication_classes = (JWTAuthentication,)

    def get_object(self, request, pk=None):
        obj = get_object_or_404(List, pk=pk)
        self.check_object_permissions(request, obj)
        return obj

    def get(self, request, pk=None):
        serializer = ListSerializer(self.get_object(request, pk), many=False)
        return Response(serializer.data)

    def put(self, request, pk=None):
        serializer = TaskSerializer(self.get_object(request, pk), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk=None):
        self.get_object(request, pk).delete()
        return Response(status=HTTP_204_NO_CONTENT)

class TaskView(GenericAPIView):
    serializer_class = TaskSerializer
    permission_classes = (MyOwnPermissions,)
    authentication_classes = (JWTAuthentication,)

    def get_queryset(self, request):
        search = request.query_params.get('task_list')
        tasks = Task.objects.all()
        if not (request.user.is_staff or request.user.is_superuser):
            tasks = Task.objects.filter(task_list__owner=request.user)
        if (search := request.query_params.get("task_list")) is not None:
            return tasks.filter(task_list=search)
        return tasks
            
    
    def get(self, request, format=None):
        serializer = TaskSerializer(self.get_queryset(request), many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = TaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class TaskDetailView(GenericAPIView):
    serializer_class = TaskSerializer
    permission_classes = (MyOwnPermissions,)
    authentication_classes = (JWTAuthentication,)

    def get_queryset(self, request, pk):
        obj = get_object_or_404(Task, pk=pk)
        self.check_object_permissions(request, obj)
        return obj

    def get(self, request, pk=None):
        serializer = TaskSerializer(self.get_queryset(request, pk), many=False)
        return Response(serializer.data)
    
    def put(self, request, pk=None):
        serializer = TaskSerializer(self.get_queryset(request, pk), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk=None):
        self.get_queryset(request, pk).delete()
        return Response(status=HTTP_204_NO_CONTENT)