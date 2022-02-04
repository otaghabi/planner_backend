from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User, Advisor, Student


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'password',
            'first_name',
            'last_name',
            'national_code',
            'phone_number',
            'age',
            'avatar'
        )

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    def validate(self, attrs):
        self.token = attrs['refresh_token']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')


class CreateAdvisorSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Advisor
        fields = (
            'user',
            'bio',
            'subscription_fee'
        )

    def save(self, **kwargs):
        """
           kwargs should contain `user` object
           it should be evaluated from AuthToken
           """
        user = kwargs.get('user')
        assert user is not None, "`user` is None"
        return super().save(user=user)


class CreateStudentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    advisor = serializers.PrimaryKeyRelatedField(queryset=Advisor.objects.all(), required=False)

    class Meta:
        model = Student
        fields = (
            'user',
            'advisor',
            'grade',
        )

    def save(self, **kwargs):
        """
           kwargs should contain `user` object
           it should be evaluated from AuthToken
           """
        user = kwargs.get('user')
        assert user is not None, "`user` is None"
        return super().save(user=user)


class AdvisorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Advisor
        fields = (
            'user',
            'id',
            'bio',
            'subscription_fee'
        )


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Student
        fields = (
            'user',
            'id',
            'grade'
        )

