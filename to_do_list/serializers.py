from rest_framework.serializers import ModelSerializer, ReadOnlyField, ValidationError, CharField
from .models import List, Task

class ListSerializer(ModelSerializer):
    class Meta:
        model = List
        fields = '__all__'
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['owner'] = instance.owner.username
        return rep

class TaskSerializer(ModelSerializer):
    class Meta: 
        model = Task
        fields = '__all__'
    
    def validate_priority(self, value):
        priorities = ['A', 'B', 'C', 'D', 'E']
        if value not in priorities:
            raise ValidationError('Priority has to be letter: A, B, C, D or E')
        return value   

    def to_representation(self, instance):
        rep = super().to_representation(instance) 
        rep['list'] = instance.list.title
        rep['owner'] = instance.owner.username

        return rep
    

