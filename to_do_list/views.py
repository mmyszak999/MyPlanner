from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import status
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import ListSerializer, TaskSerializer
from .models import List, Task
from .permissions import MyOwnPermissions


class ListView(GenericAPIView):
    serializer_class = ListSerializer
    permission_classes = (MyOwnPermissions,)
    authentication_classes = (JWTAuthentication,)
    
    def get_queryset(self, request):
        if request.user.is_staff or request.user.is_superuser:
            return get_list_or_404(List)
        return get_list_or_404(List, owner=request.user)

    def get(self, request, format=None):
        serializer = ListSerializer(self.get_queryset(request), many=True)
        return Response(serializer.data, status=200)

    def post(self, request, format=None):
        serializer = ListSerializer(data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

class ListDetailView(GenericAPIView):
    serializer_class = ListSerializer
    permission_classes = (MyOwnPermissions,)
    authentication_classes = (JWTAuthentication,)

    def get_queryset(self, request, pk):
        obj = get_object_or_404(List, pk=pk)
        self.check_object_permissions(request, obj)
        return obj

    def get(self, request, pk=None, format=None):
        serializer = ListSerializer(self.get_queryset(request, pk), many=False)
        return Response(serializer.data)

    def put(self, request, pk=None, format=None):
        list = List.objects.get(pk=pk)
        serializer = ListSerializer(list, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk=None, format=None):
        self.get_queryset(request, pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TaskView(GenericAPIView):
    serializer_class = TaskSerializer
    permission_classes = (MyOwnPermissions,)
    authentication_classes = (JWTAuthentication,)

    def get_queryset(self, request):
        search = request.query_params.get('task_list')
        if search is not None:
            if request.user.is_staff or request.user.is_superuser:
                return get_list_or_404(Task, task_list=search)
            return get_list_or_404(Task, task_list=search, owner=request.user)
        else:
            if request.user.is_staff or request.user.is_superuser:
                return get_list_or_404(Task)
            return get_list_or_404(Task, owner=request.user)
            
    
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

    def get(self, request, pk=None, format=None):
        serializer = TaskSerializer(self.get_queryset(request, pk), many=False)
        return Response(serializer.data)
    
    def put(self, request, pk=None, format=None):
        serializer = TaskSerializer(self.get_queryset(request, pk), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk=None, format=None):
        self.get_queryset(request, pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)