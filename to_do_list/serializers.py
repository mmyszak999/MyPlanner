from rest_framework.serializers import (
    Serializer,
    ModelSerializer,
    CharField,
    ReadOnlyField,
    ChoiceField,
    PrimaryKeyRelatedField,
    SerializerMethodField,
    IntegerField,
    BaseSerializer,
    CurrentUserDefault
)

from to_do_list.enums import PRIORITIES
from to_do_list.models import List, Task
from to_do_list.validation import PriorityValidation, TaskAssignmentValidation


class ListInputSerializer(Serializer):

    title = CharField()

    '''def save(self, **kwargs):
        kwargs['owner'] = self.context['request'].user
        return super().save(**kwargs)

    def create(self, validated_data):
        return List.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        return instance'''


class ListOutputSerializer(ModelSerializer):
    owner_name = ReadOnlyField(source='owner.username')

    class Meta:
        model = List
        fields = ('id', 'title', 'owner', 'owner_name')


class TaskInputSerializer(Serializer):

    id = ReadOnlyField()
    body = CharField()
    task_list = PrimaryKeyRelatedField(validators=[TaskAssignmentValidation()], queryset=List.objects.all())
    priority = ChoiceField(PRIORITIES, validators=[PriorityValidation()])

    def create(self, validated_data):
        return Task.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.body = validated_data.get('body', instance.body)
        instance.priority = validated_data.get('priority', instance.priority)
        instance.save()
        return instance


class TaskOutputSerializer(ModelSerializer):
    task_owner = ReadOnlyField(source='task_list.owner.username')
    list_name = ReadOnlyField(source='task_list.title')

    class Meta:
        model = Task
        fields = ('id', 'body', 'task_list', 'priority', 'task_owner', 'list_name')