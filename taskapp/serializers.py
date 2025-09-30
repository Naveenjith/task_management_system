from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    assigned_to_username = serializers.ReadOnlyField(source='assigned_to.username')

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'due_date', 'assigned_to_username']

class TaskCompletionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['completion_report', 'worked_hours']
        
    def validate(self, data):
        if not data.get('completion_report'):
            raise serializers.ValidationError("Completion report is required.")
        if data.get('worked_hours') is None:
            raise serializers.ValidationError("Worked hours are required.")
        return data
        
class TaskReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['completion_report', 'worked_hours']