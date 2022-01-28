from django.contrib.auth import authenticate
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken


from api.serializers.accounts_serializers import LoginSerializer, UserSerializer, LogoutSerializer
from utils.response import *


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = authenticate(email=serializer.validated_data['email'],
                                password=serializer.validated_data['password'])
            token = RefreshToken.for_user(user)
            user = UserSerializer(user)
            context = {
                'refresh_token': str(token),
                'access_token': str(token.access_token),
                'user': user.data
            }
            return successful_response(data=context)
        return unsuccessful_response(errors=serializer.errors)


class RegistrationView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return successful_response(status_code=status.HTTP_201_CREATED)
        return unsuccessful_response(serializer.errors)


class LogoutView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return successful_response()
        return unsuccessful_response(errors=serializer.errors)


class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return successful_response(data=serializer.data)

    def partial_update(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)
            return successful_response(serializer.data)
        return unsuccessful_response(errors=serializer.errors)
