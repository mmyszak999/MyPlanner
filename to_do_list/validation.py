from typing import (
    Any,
    OrderedDict
)

from rest_framework.serializers import ValidationError
from rest_framework.request import Request

from to_do_list.enums import PRIORITIES
from to_do_list.models import List


class PriorityValidation:

    def __call__(self, value: OrderedDict[str, Any]):
        priorities = [_priority[0] for _priority in PRIORITIES]
        task_priority = value
        if task_priority not in priorities:
            raise ValidationError('Priority has to be letter: A, B, C, D or E')

class TaskAssignmentValidation:
    requires_context = True

    def __call__(self, value: OrderedDict[str, Any], obj_data: OrderedDict[str, Any]) -> None:
        list_owner = value.owner
        current_user = obj_data.context['request'].user
        
        if not (current_user == list_owner or current_user.is_superuser):
            raise ValidationError("You are not the list owner")