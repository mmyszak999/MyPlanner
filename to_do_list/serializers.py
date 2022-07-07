from rest_framework.serializers import (
    Serializer,
    ModelSerializer,
    CharField,
    ReadOnlyField,
    ChoiceField,
    PrimaryKeyRelatedField
)

from to_do_list.enums import PRIORITIES
from to_do_list.models import List, Task
from to_do_list.validation import PriorityValidation, TaskAssignmentValidation


class ListInputSerializer(ModelSerializer):

    class Meta:
        model = List
        fields = ('id', 'title', 'owner')


class ListOutputSerializer(Serializer):
    id = ReadOnlyField()
    title = CharField()
    owner = ReadOnlyField(source='owner.id')
    owner_name = ReadOnlyField(source='owner.username')

    def save(self, **kwargs):
        kwargs['owner'] = self.context['request'].user
        return super().save(**kwargs)

    def create(self, validated_data):
        return List.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        return instance


class TaskInputSerializer(ModelSerializer):

    class Meta:
        model = Task
        fields = ('id', 'body', 'task_list', 'priority')
        validators = [PriorityValidation(), TaskAssignmentValidation()]


class TaskOutputSerializer(Serializer):
    id = ReadOnlyField()
    body = CharField()
    task_list = PrimaryKeyRelatedField(validators=[TaskAssignmentValidation()], read_only=True)
    priority = ChoiceField(PRIORITIES, validators=[PriorityValidation()])
    task_owner = ReadOnlyField(source='task_list.owner.username')
    list_name = ReadOnlyField(source='task_list.title')

    def save(self, **kwargs):
        return super().save(**kwargs)

    def create(self, validated_data):
        return Task.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.body = validated_data.get('body', instance.body)
        instance.priority = validated_data.get('priority', instance.priority)
        instance.save()
        return instance