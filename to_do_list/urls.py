import dataclasses
from django.urls import path

from .views import *

urlpatterns = [
    path('lists/', ListView.as_view()),
    path('lists/<str:pk>', ListDetailView.as_view()),
    path('lists/<str:pk>/tasks_in_list', TasksInListView.as_view()),
    path('tasks/', TaskView.as_view()),
    path('tasks/<str:pk>/', TaskDetailView.as_view())
]
