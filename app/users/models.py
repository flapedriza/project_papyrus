from __future__ import unicode_literals

import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from rest_framework.authtoken.models import Token

from .managers import DefaultUserManager


class User(AbstractBaseUser, PermissionsMixin):

    USERNAME_FIELD = 'email'

    objects = DefaultUserManager()

    uuid = models.UUIDField(primary_key=True, editable=False, blank=True,
                            default=uuid.uuid4)
    email = models.EmailField('email address', unique=True)

    first_name = models.CharField(max_length=32, blank=True)
    last_name = models.CharField(max_length=32, blank=True)

    is_staff = models.BooleanField('staff', default=False)
    is_active = models.BooleanField('active', default=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "[{}] {} {}".format(self.email, self.first_name, self.last_name)

    @property
    def token(self):
        token = Token.objects.get(user=self)
        return token

    def get_short_name(self):
        return self.email