from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Task
from .serializers import TaskSerializer, TaskCompletionSerializer, TaskReportSerializer
from .permissions import IsUser,IsAdminOrSuperAdmin



#List Tasks for logged-in user
class TaskListAPIView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user)


#Complete Task for assigned user
class TaskCompleteAPIView(generics.UpdateAPIView):
    serializer_class = TaskCompletionSerializer
    permission_classes = [IsAuthenticated, IsUser]
    queryset = Task.objects.all()

    def update(self, request, *args, **kwargs):
        task = self.get_object()
        serializer = self.get_serializer(task, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(status='Completed')
        return Response(serializer.data, status=status.HTTP_200_OK)


#Task Report for Admin & SuperAdmin
class TaskReportAPIView(generics.RetrieveAPIView):
    serializer_class = TaskReportSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSuperAdmin]
    queryset = Task.objects.filter(status='Completed')
