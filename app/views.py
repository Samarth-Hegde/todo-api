from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import IntegrityError
from .models import Todo, History
from .serializers import TodoSerializer, HistorySerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        todo = Todo.objects.get(id=response.data['id'])
        History.objects.create(action='add', todo_title = todo.title, todo_id=todo.id, data={'title': todo.title, 'description': todo.description, 'completed': todo.completed})
        return response

    def update(self, request, *args, **kwargs):
        todo = self.get_object()
        old_data = {'title': todo.title, 'description': todo.description, 'completed': todo.completed}
        response = super().update(request, *args, **kwargs)
        new_data = {'title': request.data.get('title', todo.title), 'description': request.data.get('description', todo.description), 'completed': request.data.get('completed', todo.completed)}
        History.objects.create(action='edit',todo_title = todo.title, todo_id=todo.id, data={'old': old_data, 'new': new_data})
        return response

    def partial_update(self, request, *args, **kwargs):
        todo = self.get_object()
        old_data = {'title': todo.title, 'description': todo.description, 'completed': todo.completed}
        response = super().partial_update(request, *args, **kwargs)
        new_data = {'title': request.data.get('title', todo.title), 'description': request.data.get('description', todo.description), 'completed': request.data.get('completed', todo.completed)}
        History.objects.create(action='edit',todo_title = todo.title, todo_id=todo.id, data={'old': old_data, 'new': new_data})
        return response

    def destroy(self, request, *args, **kwargs):
        todo = self.get_object()
        History.objects.create(action='delete',todo_title = todo.title, todo_id=todo.id, data={'title': todo.title, 'description': todo.description, 'completed': todo.completed})
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        todo = self.get_object()
        todo.completed = True
        todo.save()
        History.objects.create(action='complete',todo_title = todo.title, todo_id=todo.id, data={'title': todo.title, 'description': todo.description, 'completed': todo.completed})
        serializer = TodoSerializer(todo)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def history(self, request): 
        last_ten = History.objects.order_by('-created_at')[:10]
        serializer = HistorySerializer(last_ten, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def undo(self, request, pk=None):
        history = get_object_or_404(History, pk=pk)
        if history.action == 'add':
            Todo.objects.get(id=history.todo_id).delete()
        elif history.action == 'delete':
            if Todo.objects.filter(id=history.todo_id).exists():
                return Response({'error': 'ID conflict'}, status=409) 
            try:
                Todo.objects.create(id=history.todo_id, **history.data)
            except IntegrityError:
                return Response({'error': 'ID conflict'}, status=409)
        elif history.action == 'edit':
            todo = Todo.objects.get(id=history.todo_id)
            for key, value in history.data['old'].items():
                setattr(todo, key, value)
            todo.save()
        elif history.action == 'complete':
            todo = Todo.objects.get(id=history.todo_id)
            todo.completed = False
            todo.save()
        else:
            Response({'status':'failed'})
        return Response({'status': 'success'})  