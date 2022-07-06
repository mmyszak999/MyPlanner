from subprocess import list2cmdline
from rest_framework.serializers import ValidationError
from to_do_list.enums import PRIORITIES

from to_do_list.models import Task, List

class PriorityValidation():
    requires_context = True

    def __init__(self):
        pass

    def __call__(self, value, obj_data):
        priorities = [_priority[0] for _priority in PRIORITIES]
        task_priority = obj_data.initial_data['priority']
        if task_priority not in priorities:
            raise ValidationError(f'Priority has to be letter: A, B, C, D or E')

class TaskAssignmentValidation():
    requires_context = True

    def __init__(self):
        pass

    def __call__(self, value, obj_data):
        task_list = obj_data.initial_data['task_list']
        list_owner = List.objects.get(id=task_list).owner
        current_user = obj_data.context['request'].user
        print(current_user, list_owner, task_list)
        
        if (current_user == list_owner or current_user.is_superuser) is False:
            raise ValidationError(f"You are not the list owner")