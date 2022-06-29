from rest_framework.serializers import ValidationError
from to_do_list.enums import PRIORITIES

from to_do_list.models import Task, List

class PriorityValidation(object):
    requires_context = True

    def __init__(self, object):
        self.object = object

    def __call__(self, value, obj_data):
        priorities = [x[0] for x in PRIORITIES]
        task_priority = obj_data.initial_data['priority']
        if task_priority not in priorities:
            raise ValidationError(f'Priority has to be letter: A, B, C, D or E')

class TaskAssignmentValidation(object):
    requires_context = True

    def __init__(self, object):
        self.object = object

    def __call__(self, value, obj_data):
        task_list = obj_data.initial_data['task_list']
        list_owner = List.objects.get(id=task_list).owner
        current_user = obj_data.context['request'].user

        if not current_user.is_superuser:
            if current_user is not list_owner:
                raise ValidationError(f"You are not the list owner")