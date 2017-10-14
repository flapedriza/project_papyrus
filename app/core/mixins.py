from django.db import models


class TimeStampedModelMixin(models.Model):
    """
    Abstract Mixin model to add timestamp
    """
    # Timestamp
    created = models.DateTimeField(u"Date created", auto_now_add=True)
    updated = models.DateTimeField(
        u"Date updated", auto_now=True, db_index=True)

    class Meta:
        abstract = True
