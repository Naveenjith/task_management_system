from django.urls import path
from .views import TaskListAPIView, TaskCompleteAPIView, TaskReportAPIView

urlpatterns = [
    path('api/task/', TaskListAPIView.as_view(), name='task-list'),
    path('api/task/<int:pk>/completeview/', TaskCompleteAPIView.as_view(), name='task-completion'),
    path('api/task/<int:pk>/reportview/', TaskReportAPIView.as_view(), name='task-reports'),
]