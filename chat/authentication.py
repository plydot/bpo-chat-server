from django.contrib.auth.backends import ModelBackend

from chat.models import Users


class AuthBackend(ModelBackend):

    def authenticate(self, request, phone=None, password=None, username=None, **kwargs):
        try:
            if phone is None:
                phone = username
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
