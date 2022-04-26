from django.db import models

PRIORITIES = [
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D'),
    ('E', 'E')
]

class List(models.Model):
    title = models.TextField(max_length=60, null=False)
    owner = models.ForeignKey('auth.User', related_name='list', on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return self.title[0:50]

class Task(models.Model):
    body = models.TextField(null=False, blank=True, max_length=75)
    priority = models.CharField(max_length=3, choices=PRIORITIES)
    list = models.ForeignKey(List, on_delete=models.CASCADE)
    owner = models.ForeignKey('auth.User', related_name='task', on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return self.body[0:50]
    
