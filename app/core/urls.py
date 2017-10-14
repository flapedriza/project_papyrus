from django.conf.urls import url
from rest_framework import routers

from app.core.views import TaskViewset, TagViewSet, ProjectViewSet

router = routers.SimpleRouter()
router.register(r"tasks", TaskViewset, base_name="tasks")
router.register(r"tags", TagViewSet, base_name="tags")
router.register(r"projects", ProjectViewSet, base_name="projects")

urlpatterns = router.urls
