import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class Users(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_active = models.BooleanField(default=True)
    avatar = models.ImageField()
    bio = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True, auto_now=True)
    date_joined = models.DateTimeField(blank=True, null=True, auto_now=True)
    last_login = models.DateTimeField(blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(unique=True, max_length=50, blank=False, null=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    socket_sio = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.phone

    def __unicode__(self):
        return self.__str__()

    class Meta:
        db_table = 'users'
        verbose_name_plural = 'Users'
        managed = False
