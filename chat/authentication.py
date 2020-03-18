from django.contrib.auth import authenticate
from django.contrib.auth.backends import ModelBackend
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.views import TokenObtainPairView

from chat.models import Users


class AuthBackend(ModelBackend):

    def authenticate(self, request, phone=None, password=None, **kwargs):
        try:
            user = Users.objects.get(phone=phone)
            if user.check_password(password):
                return user
            else:
                return None
        except Exception:
            return None

    def get_user(self, user_id):
        try:
            return Users.objects.get(id=user_id)
        except Users.DoesNotExist:
            return None
