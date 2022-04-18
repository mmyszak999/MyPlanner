from django.forms import IntegerField
from rest_framework.serializers import ModelSerializer, ReadOnlyField, ValidationError
from .models import PRIORITIES, List, Task

class ListSerializer(ModelSerializer):
    owner = ReadOnlyField(source='owner.username')
    class Meta:
        model = List
        fields = '__all__'

class TaskSerializer(ModelSerializer):
    #list = ReadOnlyField(source='List.title')
    class Meta:
        model = Task
        fields = '__all__'
    
    def validate_priority(self, value):
        priorities = ['A', 'B', 'C', 'D', 'E']
        if value not in priorities:
            raise ValidationError('Priority has to be letter: A, B, C, D or E')
        return value    
    

