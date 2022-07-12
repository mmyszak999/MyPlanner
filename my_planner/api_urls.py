from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from to_do_list import views

app_name = 'api'

urlpatterns = [
    path('lists/', views.ListView.as_view(), name='list-lists'),
    path('lists/<int:pk>', views.ListDetailView.as_view(), name='list-single-list'),
    path('lists/<int:pk>/tasks',views.TaskView.as_view(), name='list-tasks-in-list'),
    path('lists/<int:pk>/tasks/<int:task_pk>',views.TaskDetailView.as_view(), name='list-single-task-in-list'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
