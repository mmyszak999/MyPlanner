from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from to_do_list import views

urlpatterns = [
    path('lists/', views.ListView.as_view()),
    path('lists/<int:pk>', views.ListDetailView.as_view()),
    path('tasks/', views.TaskView.as_view()),
    path('tasks/<int:pk>/', views.TaskDetailView.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
