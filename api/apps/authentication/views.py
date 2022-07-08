from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.apps.authentication.models import User


class AuthenticationViewSet(ModelViewSet):
    queryset = User.objects.all()

    @action(methods=['post'], detail=False)
    def login(self, request):
        user = authenticate(request, email=request.data['email'], password=request.data['password'])
        if user is not None:
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(methods=['get'], detail=True)
    def logout(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True)
    def register(self, request):
        User.objects.create_user(request.data['email'], request.data['password'])
        return Response(status=status.HTTP_201_CREATED)

    @action(methods=['patch'], detail=True)
    def reset_password(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        user = request.user
        user.set_password(request.data['password'])
        user.save()
        return Response(status=status.HTTP_200_OK)

    @action(methods=['patch'], detail=True)
    def authorize_creator(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        # TODO: some more logic here
        user = request.user
        user.type = User.UserType.CREATOR
        user.save()
        return Response(status=status.HTTP_200_OK)
