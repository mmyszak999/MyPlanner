from rest_framework.serializers import ModelSerializer, SerializerMethodField

from to_do_list.models import List, Task
from to_do_list.validation import PriorityValidation, TaskAssignmentValidation

class ListSerializer(ModelSerializer):
    list_owner = SerializerMethodField()

    class Meta:
        model = List
        fields = ['id', 'title', 'owner', 'list_owner']

    def get_list_owner(self, obj):
        return obj.owner.username


class TaskInputSerializer(ModelSerializer):
    class Meta: 
        model = Task
        fields = ['id', 'body', 'task_list', 'priority']
        validators = [PriorityValidation(), TaskAssignmentValidation()]


class TaskOutputSerializer(ModelSerializer):
    list_name = SerializerMethodField()
    task_owner = SerializerMethodField()
    class Meta: 
        model = Task
        fields = ['id', 'body', 'task_owner', 'task_list', 'list_name', 'priority']
        validators = [PriorityValidation(), TaskAssignmentValidation()]

    def get_list_name(self, obj):
        return obj.task_list.title
    
    def get_task_owner(self, obj):
        return obj.task_list.owner.username