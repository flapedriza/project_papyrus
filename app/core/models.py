from django.db import models
from .mixins import TimeStampedModelMixin


class Project(TimeStampedModelMixin):
    users = models.ManyToManyField("users.User")
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=16, null=True, blank=True)

    def __str__(self):
        return "Project %s " % self.name


class Tag(TimeStampedModelMixin):
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=16, null=True, blank=True)

    def __str__(self):
        return "Tag %s" % self.name


class Task(TimeStampedModelMixin):

    user = models.ForeignKey("users.User", related_name="tasks")
    project = models.ForeignKey("Project", null=True, blank=True)

    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    priority = models.PositiveIntegerField(default=0)

    completed = models.BooleanField(default=False)

    expiration_date = models.DateTimeField(null=True, blank=True)

    tags = models.ManyToManyField("Tag", blank=True)


