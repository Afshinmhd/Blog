from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import password_validation


def clean_email(value):
    user = User.objects.filter(email=value)
    if user:
        raise serializers.ValidationError('This email already exist')
    return value

    
class RegisterSerializer(serializers.ModelSerializer):
    """
        This class used to serialize input data
    """
    password2 = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')
        extra_kwargs = {
            'password': {'write_only': True},
            'password2': {'write_only': True},
            'email': {'validators': (clean_email,)}
        }

    
    def validate_username(self, value):
        user = User.objects.filter(username=value)
        if user:
            raise serializers.ValidationError()
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'error': 'passwords must be matched'})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        return User.objects.create(**validated_data)
