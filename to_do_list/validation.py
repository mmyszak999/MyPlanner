from typing import (
    Any,
    OrderedDict
)

from rest_framework.serializers import ValidationError
from to_do_list.enums import PRIORITIES

from to_do_list.models import List

class PriorityValidation():
    requires_context = True

    def __call__(self, value: OrderedDict[str, Any], obj_data: OrderedDict[str, Any]):
        priorities = [_priority[0] for _priority in PRIORITIES]
        task_priority = obj_data.initial_data['priority']
        if task_priority not in priorities:
            raise ValidationError('Priority has to be letter: A, B, C, D or E')

class TaskAssignmentValidation():
    requires_context = True

    def __call__(self, value: OrderedDict[str, Any], obj_data: OrderedDict[str, Any]):
        task_list = obj_data.initial_data['task_list']
        list_owner = List.objects.get(id=task_list).owner
        current_user = obj_data.context['request'].user
        
        if not (current_user == list_owner or current_user.is_superuser):
            raise ValidationError("You are not the list owner")