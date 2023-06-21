from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from api import views

app_name = 'api'

urlpatterns = [
    path('lists/', views.ListView.as_view({'post': 'create'}), name='list-lists'),
    path('lists/<int:pk>', views.ListDetailView.as_view({'put': 'update'}), name='list-single-list'),
    path('lists/<int:pk>/tasks', views.TaskView.as_view({'post': 'create'}), name='list-tasks-in-list'),
    path('lists/<int:pk>/tasks/<int:task_pk>', views.TaskDetailView.as_view({'put': 'update'}), name='list-single-task-in-list'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
