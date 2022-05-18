from django.urls import path

from to_do_list.views import *

urlpatterns = [
    path('lists/', ListView.as_view()),
    path('lists/<int:pk>', ListDetailView.as_view()),
    path('tasks/', TaskView.as_view()),
    path('tasks/<int:pk>/', TaskDetailView.as_view()),
]
