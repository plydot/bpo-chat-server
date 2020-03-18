import uuid

import bcrypt
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, Group, Permission
from django.db import models

from chat.managers import CustomUserManager


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

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.phone

    def __unicode__(self):
        return self.__str__()

    def set_password(self, raw_password):
        self.password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt(rounds=10)).decode("utf-8")
        self._password = raw_password

    def check_password(self, raw_password):
        return bcrypt.checkpw(raw_password.encode('utf-8'), self.password.encode('utf-8'))

    class Meta:
        db_table = 'users'
        verbose_name_plural = 'Users'


class GroupUser(models.Model):
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING)
    users = models.ForeignKey(Users, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'users_groups'
        managed = False


class UsersPermissions(models.Model):
    users = models.ForeignKey(Users, on_delete=models.DO_NOTHING)
    permission = models.ForeignKey(Permission, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'users_user_permissions'
        managed = False
