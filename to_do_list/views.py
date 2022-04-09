from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.parsers import JSONParser, ParseError

from to_do_list.serializers import ListSerializer, TaskSerializer

from .models import List, Task

class ListView(APIView):
    def get(self, request, format=None):
        lists = List.objects.all()
        serializer = ListSerializer(lists, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ListSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListDetailView(APIView):
    def get(self, request, pk=None, format=None):
        single_list = List.objects.get(pk=pk)
        serializer = ListSerializer(single_list, many=False)
        return Response(serializer.data)

    def put(self, request, pk=None, format=None):
        list = List.objects.get(pk=pk)
        serializer = ListSerializer(list, many=False)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, format=None):
        list = List.objects.get(pk=pk)
        list.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TasksInListView(APIView):
    def get(self, request, pk=None, format=None):
        tasks = Task.objects.filter(list=pk)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

class TaskView(APIView):
    def get(self, request, format=None):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = TaskSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskDetailView(APIView):
    def get(self, request, pk=None, format=None):
        task = Task.objects.get(pk=pk)
        serializer = TaskSerializer(task, many=False)
        return Response(serializer.data)
    
    def put(self, request, pk=None, format=None):
        task = Task.objects.get(pk=pk)
        serializer = TaskSerializer(Task, many=False)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, format=None):
        task = Task.objects.get(pk=pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)








