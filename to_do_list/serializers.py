from rest_framework.serializers import ModelSerializer
from .models import List, Task

class ListSerializer(ModelSerializer):
    class Meta:
        model = List
        fields = '__all__'

class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'