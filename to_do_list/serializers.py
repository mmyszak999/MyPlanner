from rest_framework.serializers import ModelSerializer, ValidationError, SerializerMethodField, HiddenField, CurrentUserDefault
from .models import List, Task
from .enums import PRIORITIES

class ListSerializer(ModelSerializer):
    list_owner = SerializerMethodField()

    class Meta:
        model = List
        fields = ['id', 'title', 'owner', 'list_owner']

    def get_list_owner(self, obj):
        return obj.owner.username


class TaskSerializer(ModelSerializer):
    list_name = SerializerMethodField()
    task_owner = SerializerMethodField()
    class Meta: 
        model = Task
        fields = ['id', 'body', 'task_owner', 'task_list', 'list_name', 'priority']
    
    def validate(self, attrs):
        priorities = []
        for i in range(0, 5):
            priorities.append(PRIORITIES[i][0])
            
        task_priority = attrs.get('priority')
        task_list = attrs.get('task_list')
        request = self.context.get('request')
        list_owner = List.objects.get(id=task_list.id).owner

        if request.user.is_superuser is False:
            if request.user is not list_owner:
                raise ValidationError(f"You are not the list owner")
            pass
        
        if task_priority not in ['A', 'B', 'C', 'D', 'E']:
            raise ValidationError(f'Priority has to be letter: A, B, C, D or E')
        pass

        return attrs

    def get_list_name(self, obj):
        return obj.task_list.title
    
    def get_task_owner(self, obj):
        return obj.task_list.owner.username