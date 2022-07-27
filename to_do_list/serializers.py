from rest_framework.serializers import (
    Serializer,
    ModelSerializer,
    CharField,
    ReadOnlyField,
    ChoiceField,
    PrimaryKeyRelatedField,
)

from to_do_list.enums import PRIORITIES
from to_do_list.models import List, Task
from to_do_list.validation import PriorityValidation, TaskAssignmentValidation


class ListInputSerializer(Serializer):

    title = CharField()


class ListOutputSerializer(ModelSerializer):
    owner_name = ReadOnlyField(source='owner.username')

    class Meta:
        model = List
        fields = ('id', 'title', 'owner', 'owner_name')
        read_only_fields = fields


class TaskInputSerializer(Serializer):

    id = ReadOnlyField()
    body = CharField()
    task_list = PrimaryKeyRelatedField(validators=[TaskAssignmentValidation()], queryset=List.objects.all())
    priority = ChoiceField(PRIORITIES, validators=[PriorityValidation()])


class TaskOutputSerializer(ModelSerializer):
    task_owner = ReadOnlyField(source='task_list.owner.username')
    list_name = ReadOnlyField(source='task_list.title')

    class Meta:
        model = Task
        fields = ('id', 'body', 'task_list', 'priority', 'task_owner', 'list_name')
        read_only_fields = fields