from django.contrib import admin

from .models import List, Task

class ListAdmin(admin.ModelAdmin):
    pass

admin.site.register(List, ListAdmin)

class TaskAdmin(admin.ModelAdmin):
    pass

admin.site.register(Task, TaskAdmin)

