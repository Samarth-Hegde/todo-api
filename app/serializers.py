from rest_framework import serializers
from .models import Todo, History

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id', 'title', 'description', 'completed', 'created_at', 'updated_at']

class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ['id', 'action', 'todo_id', 'created_at']