from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.decorators import action

from to_do_list.serializers import ListSerializer, TaskSerializer

from .utils import *
from .models import List, Task

class ListViewSet(ModelViewSet):
    serializer_class = ListSerializer
    queryset = List.objects.all()

    @action(detail=False, methods=['GET'])
    def get_lists(self, request):
        lists = List.objects.all()
        serializer = ListSerializer(instance=lists, data=request.data)
        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response(serializer.errors,
            status=HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['GET'])
    def get_single_list(self, request, pk=id):
        list = List.objects.get(pk=id)
        serializer = ListSerializer(instance=list, data=request.data)
        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response(serializer.errors,
            status=HTTP_400_BAD_REQUEST)



