from typing_extensions import Required
from django.db import models
from django.urls import reverse

from .enums import PRIORITIES

class List(models.Model):
    title = models.TextField(max_length=60)
    owner = models.ForeignKey('auth.User', related_name='list', on_delete=models.CASCADE)

    @property
    def absolute_url(self) -> str:
        return reverse("api:list-lists")
    
    def __str__(self):
        return self.title[0:50]

class Task(models.Model):
    body = models.TextField(max_length=75)
    task_list = models.ForeignKey(List, on_delete=models.CASCADE, related_name='tasklist')
    priority = models.CharField(max_length=1, choices=PRIORITIES)

    def __str__(self):
        return self.body[0:50]
    
