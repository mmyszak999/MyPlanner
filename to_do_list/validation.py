from rest_framework.serializers import ValidationError
from rest_framework.request import Request

from to_do_list.models import List


def TaskAssignmentValidation(request: Request, instance: List) -> None:
    list_owner = instance.owner
    current_user = request.user

    if not (current_user == list_owner or current_user.is_superuser):
        raise ValidationError("You are not the list owner")