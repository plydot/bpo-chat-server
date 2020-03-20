import requests
from django.http import Http404
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from api.serializers import UsersSerializer, RegistrationSerializer
from chat.models import Users


class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    authentication_classes = [JWTAuthentication,]
    lookup_field = 'phone'

    def create(self, request, *args, **kwargs):
        q = self.request.query_params.get("q")
        if q == '1':
            users = Users.objects.filter(phone__in=request.data)
            serializer = self.get_serializer(users, many=True)
            return Response(serializer.data)
        else:
            return super().create(request, *args, **kwargs)


class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = (AllowAny,)
    authentication_classes = []
    lookup_field = 'phone'

    def create(self, request, *args, **kwargs):
        if request.data['phone'].startswith("0"):
            request.data['phone'] = '256{}'.format(request.data['phone'][1:]).replace("+", "")
        serializer = self.get_serializer(data=request.data)
        errors = []
        data = {}
        if not serializer.is_valid():
            for k, v in serializer.errors.items():
                errors.append(str(v[0]))
            data['success'] = False
            return Response({'data': data, 'errors': errors}, status=status.HTTP_200_OK)

        user = serializer.save()
        user.set_password(user.password)
        user.save()
        data['success'] = True
        return Response({'data': data, 'errors': errors}, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        available = True
        try:
            instance = self.get_object()
            if instance is None:
                raise Http404
        except Http404:
            available = False
        return Response(available, status=status.HTTP_200_OK)
