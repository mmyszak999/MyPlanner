from rest_framework.serializers import ModelSerializer, ReadOnlyField
from .models import List, Task

class ListSerializer(ModelSerializer):
    owner = ReadOnlyField(source='owner.username')
    class Meta:
        model = List
        fields = '__all__'

class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'