from rest_framework import viewsets

from app.core.models import Task, Project, Tag
from app.core.serializers import TaskSerializer, ProjectSerializer, TagSerializer


class TaskViewset(viewsets.ModelViewSet):
    """
    """
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


class ProjectViewSet(viewsets.ModelViewSet):
    """
    """
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(users__in=[self.request.user])


class TagViewSet(viewsets.ModelViewSet):
    """
    """
    serializer_class = TagSerializer

    def get_queryset(self):
        return Tag.objects.filter(task__user=self.request.user)
