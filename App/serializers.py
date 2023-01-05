from rest_framework import serializers
from App.models import Todo


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id', 'task_name', 'completed', 'description', 'is_deleted', 'created_at', 'updated_at']
        read_only_fields = ('id', 'created_at', 'updated_at', 'completed')


