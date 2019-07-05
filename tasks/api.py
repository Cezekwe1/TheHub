from .models import Task 
from .serializers import TaskSerializer
from rest_framework import viewsets, permissions

class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    serializer_class = TaskSerializer

    def get_queryset(self):
        return self.request.user.task_set.all()