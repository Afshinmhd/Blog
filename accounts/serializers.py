from xml.dom import ValidationErr
from rest_framework import serializers
from .models import Profile
from django.contrib.auth import password_validation
from .messages import Messages


def clean_email(value):
    user = Profile.objects.filter(email=value)
    if user:
        raise serializers.ValidationError({'Error': Messages.INCORRECT_EMAIL.value})
    return value


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class RegisterSerializer(serializers.ModelSerializer):
    """
        This class used to serialize input data
    """
    class Meta:
        model = Profile
        fields = ('username', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'validators': (clean_email,)}
        }
   
    def validate_username(self, value):
        user = Profile.objects.filter(username=value)
        if user:
            raise serializers.ValidationError({'Error': Messages.INCORRECT_USERNAME.value})
        return value

    def validate(self, attrs):
        password_validation.validate_password(attrs['password'])
        return attrs

    def create(self, validated_data):
        obj = super().create(validated_data)
        obj.set_password(validated_data['password'])
        obj.save()
        return obj


class EmailVerificationSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    code = serializers.CharField()


class EditProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['username', 'first_name', 'last_name', 'email']
        extra_kwargs = {'username': {'required': False}}


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    repeat_new_password = serializers.CharField()

    def validate_old_password(self, value):
        user = self.context.get('request').user
        if not user.check_password(value):
            raise serializers.ValidationError({'Error': Messages.INCORRECT_PASSWORD.value})
        return value

    def validate_new_password(self, value):
        password_validation.validate_password(value)
        return value

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        repeat_new_password = attrs.get('repeat_new_password')
        if not new_password == repeat_new_password:
            raise serializers.ValidationError({'error': Messages.REPEAT_NEW_PASSWORD.value})
        return attrs
