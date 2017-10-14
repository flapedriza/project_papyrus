from rest_framework import serializers
from app.users.models import User
from app.core.models import Task, Project, Tag


class TaskSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Task


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
