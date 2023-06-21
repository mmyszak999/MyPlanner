from rest_framework.serializers import (
    Serializer,
    ModelSerializer,
    CharField,
    ReadOnlyField,
    ChoiceField,
)

from api.enums import PRIORITIES
from api.models import List, Task


class ListInputSerializer(Serializer):

    title = CharField()


class ListOutputSerializer(ModelSerializer):
    owner_name = ReadOnlyField(source='owner.username')

    class Meta:
        model = List
        fields = ('id', 'title', 'owner', 'owner_name')
        read_only_fields = fields


class TaskInputSerializer(Serializer):
    body = CharField()
    priority = ChoiceField(PRIORITIES)


class TaskOutputSerializer(ModelSerializer):
    task_owner = ReadOnlyField(source='task_list.owner.username')
    list_name = ReadOnlyField(source='task_list.title')

    class Meta:
        model = Task
        fields = ('id', 'body', 'task_list', 'priority', 'task_owner', 'list_name')
        read_only_fields = fields