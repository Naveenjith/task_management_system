from django.urls import path
from .views import AdminLoginView, DashboardView, TaskReportDetailView, UserCreateView, UserUpdateView, UserDeleteView, toggle_admin_status

urlpatterns = [
    path('login/', AdminLoginView.as_view(), name='admin-login'),
    path('', DashboardView.as_view(), name='dashboard'),
    path('users/create/', UserCreateView.as_view(), name='user-create'),
    path('users/<int:pk>/update/', UserUpdateView.as_view(), name='user-update'),
    path('users/<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),
    path('users/<int:pk>/toggle-admin/', toggle_admin_status, name='user-toggle-admin'),
    path('tasks/<int:pk>/report/', TaskReportDetailView.as_view(), name='task-report-detail'),


]