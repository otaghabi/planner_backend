from django.contrib.auth import authenticate
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import Student, Advisor
from accounts.permissions import (
    IsAdvisor, IsStudent, IsHasNotAnyRoleOrStudent, IsHasNotAnyRoleOrAdvisor
)
from api.serializers.accounts_serializers import (
    StudentSerializer, AdvisorSerializer, UserSerializer,
    CreateStudentSerializer, CreateAdvisorSerializer, LoginSerializer
)
from utils.pagination import PlannerPagination
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
            content = {
                'refresh_token': str(token),
                'access_token': str(token.access_token),
                'user': user.data
            }
            return successful_response(data=content)
        return unsuccessful_response(errors=serializer.errors)


class RefreshView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TokenRefreshSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            content = {
                'access_token': serializer.validated_data['access']
            }
            return successful_response(data=content)
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


class CreateAdvisorView(generics.GenericAPIView):
    permission_classes = (IsHasNotAnyRoleOrAdvisor,)
    serializer_class = CreateAdvisorSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            advisor = Advisor.objects.get(user=request.user)
            advisor = AdvisorSerializer(advisor)
            content = {
                **advisor.data
            }
            return successful_response(data=content)
        return unsuccessful_response(errors=serializer.errors)


class CreateStudentView(generics.GenericAPIView):
    permission_classes = (IsHasNotAnyRoleOrStudent,)
    serializer_class = CreateStudentSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            student = Advisor.objects.get(user=request.user)
            student = AdvisorSerializer(student)
            content = {
                **student.data
            }
            return successful_response(data=content)
        return unsuccessful_response(errors=serializer.errors)


class AdvisorsListView(generics.GenericAPIView):
    pagination_class = PlannerPagination
    permission_classes = (IsStudent,)
    queryset = Advisor.objects.all()
    serializer_class = AdvisorSerializer

    def get(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)


class StudentListView(generics.GenericAPIView):
    pagination_class = PlannerPagination
    permission_classes = (IsAdvisor,)
    serializer_class = StudentSerializer

    def get(self, request):
        queryset = Student.objects.filter(advisor__user=request.user)
        page = self.paginate_queryset(queryset)
        serializer = self.serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)
