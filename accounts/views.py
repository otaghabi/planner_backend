from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from utils.locale import _
from utils.response import *
from .serializers import *


class LoginView(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)

            return successful_response(
                messages=_('User Login Successfully'),
                data={
                    'token': token.key
                }
            )
        return unsuccessful_response(errors=serializer.errors)


class RegistrationView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return successful_response(
                messages=_('Registration completed successfully.'),
                status_code=status.HTTP_201_CREATED
            )
        return unsuccessful_response(serializer.errors)


class Logout(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        request.user.auth_token.delete()
        return successful_response(
            messages=_('Logout was completed successfully'),
            status_code=status.HTTP_204_NO_CONTENT
        )


class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return successful_response(
            messages=_('User Profile'),
            data=serializer.data
        )

    def partial_update(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        user = self.get_object()
        if serializer.is_valid():
            self.perform_update(serializer)
            return successful_response(
                messages=_('User Profile Updated'),
            )
        return unsuccessful_response(
            errors=serializer.errors
        )
