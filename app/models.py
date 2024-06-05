import uuid
from django.db import models

class Todo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(max_length=500)

class History(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ACTION_CHOICES = [
        ('add', 'Add'),
        ('edit', 'Edit'),
        ('delete', 'Delete'),
        ('complete', 'Complete'),
    ]
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    todo_id = models.UUIDField(null=True, blank=True)
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)