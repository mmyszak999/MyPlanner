from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import NotAuthenticated
from django.shortcuts import get_object_or_404, get_list_or_404

from .serializers import ListSerializer, TaskSerializer
from .models import List, Task
from .permissions import MyOwnPermissions


class ListView(APIView):
    serializer_class = ListSerializer
    permission_classes = (MyOwnPermissions,)
    
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

class ListDetailView(APIView):
    serializer_class = ListSerializer
    permission_classes = (MyOwnPermissions,)

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

class TasksInListView(APIView):
    serializer_class = TaskSerializer
    permission_classes = (MyOwnPermissions,)

    def get_queryset(self, request, pk):
        if request.user.is_staff or request.user.is_superuser:
            return Task.objects.filter(task_list__id=pk)
        raise NotAuthenticated
         
    def get(self, request, pk=None, format=None):
        serializer = TaskSerializer(self.get_queryset(request, pk=pk), many=True)
        return Response(serializer.data)

class TaskView(APIView):
    serializer_class = TaskSerializer
    permission_classes = (MyOwnPermissions,)

    def get_queryset(self, request):
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

class TaskDetailView(APIView):
    serializer_class = TaskSerializer
    permission_classes = (MyOwnPermissions,)

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