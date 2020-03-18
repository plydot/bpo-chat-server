import requests
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.serializers import UsersSerializer, RegistrationSerializer
from chat.models import Users


class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        if request.data['phone'].startswith("0"):
            request.data['phone'] = '256{}'.format(request.data['phone'][1:]).replace("+", "")
        serializer = self.get_serializer(data=request.data)
        errors = {}
        data = {}
        if not serializer.is_valid():
            for k, v in serializer.errors.items():
                errors['{}_error'.format(k)] = str(v[0])
            data['success'] = False
            return Response({'data': data, 'errors': errors}, status=status.HTTP_200_OK)

        user = serializer.save()
        user.set_password(user.password)
        user.save()
        data['success'] = True
        return Response({'data': data, 'errors': errors}, status=status.HTTP_201_CREATED)


