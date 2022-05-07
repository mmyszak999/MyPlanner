from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import NotAuthenticated
from django.core.exceptions import ObjectDoesNotExist

from .serializers import ListSerializer, TaskSerializer
from .models import List, Task
from .permissions import MyOwnPermissions


class ListView(APIView):
    serializer_class = ListSerializer
    permission_classes = (MyOwnPermissions,)
    
    def get_queryset(self, request):
        if request.user.is_staff or request.user.is_superuser:
            return List.objects.all()
        return List.objects.filter(owner=request.user)
    
    def get(self, request, format=None):
        serializer = ListSerializer(self.get_queryset(request), many=True)
        return Response(serializer.data, status=200)

    def post(self, request, format=None):
        serializer = ListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListDetailView(APIView):
    serializer_class = ListSerializer
    permission_classes = (MyOwnPermissions,)

    def get_queryset(self, request, pk):
        single_list = List.objects.get(pk=pk)
        lists = List.objects.filter(owner=request.user)
        if MyOwnPermissions:
            try:
                single_list = lists.get(pk=pk)
            except ObjectDoesNotExist:
                raise NotAuthenticated
        return single_list
    
    def get(self, request, pk=None, format=None):
        serializer = ListSerializer(self.get_queryset(request, pk), many=False)
        return Response(serializer.data)

    def put(self, request, pk=None, format=None):
        list = List.objects.get(pk=pk)
        serializer = ListSerializer(list, data=request.data, partial=True)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

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
            return Task.objects.all()
        return Task.objects.filter(owner=request.user)
    
    def get(self, request, format=None):
        serializer = TaskSerializer(self.get_queryset(request), many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskDetailView(APIView):
    serializer_class = TaskSerializer
    permission_classes = (MyOwnPermissions,)

    def get_queryset(self, request, pk):
        single_task = Task.objects.get(pk=pk)
        tasks = Task.objects.filter(owner=request.user)
        if MyOwnPermissions:
            try:
                single_task = tasks.get(pk=pk)
            except ObjectDoesNotExist:
                raise NotAuthenticated
        return single_task

    def get(self, request, pk=None, format=None):
        serializer = TaskSerializer(self.get_queryset(request, pk), many=False)
        return Response(serializer.data)
    
    def put(self, request, pk=None, format=None):
        serializer = TaskSerializer(self.get_queryset(request, pk), data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request, pk=None, format=None):
        self.get_queryset(request, pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)








