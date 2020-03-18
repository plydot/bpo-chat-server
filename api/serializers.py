from django.db import models
from rest_framework import serializers

from chat.models import Users


class UsersSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Users
        fields = "__all__"


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Users
        fields = ('phone', 'password', 'first_name')
