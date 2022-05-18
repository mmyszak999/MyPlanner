from rest_framework.serializers import ModelSerializer, ValidationError, SerializerMethodField
from .models import List, Task

class ListSerializer(ModelSerializer):
    list_owner = SerializerMethodField()

    class Meta:
        model = List
        fields = ['id','title', 'owner', 'list_owner']

    def get_list_owner(self, obj):
        return obj.owner.username

class TaskSerializer(ModelSerializer):
    list_name = SerializerMethodField()
    task_owner = SerializerMethodField()
    class Meta: 
        model = Task
        fields = ['id','body', 'owner', 'task_owner', 'task_list','list_name', 'priority']
    
    def validate_priority(self, value):
        priorities = ['A', 'B', 'C', 'D', 'E']
        if value not in priorities:
            raise ValidationError('Priority has to be letter: A, B, C, D or E')
        return value   

    def get_list_name(self, obj):
        return obj.task_list.title
    
    def get_task_owner(self, obj):
        return obj.owner.username
    

