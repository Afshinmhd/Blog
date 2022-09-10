from rest_framework import viewsets, mixins
from .serializers import (RegisterSerializer,LoginSerializer,
                            EmailVerificationSerializer, EditProfileSerializer,
                            ChangePasswordSerializer, LogoutSerializer)
from .models import Profile
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated


class SubLoginViewSet(viewsets.ViewSet):

    def create(self, request):
        ser_data = RegisterSerializer(data=request.data)
        ser_data.is_valid(raise_exception=True)
        status, detail = Profile.sub_login(**ser_data.data)
        return Response({'detail': detail}, status=status)


class ConfirmViewSet(viewsets.ViewSet):

    def create(self, request):
        ser_data = EmailVerificationSerializer(data=request.data)
        ser_data.is_valid(raise_exception=True)
        status, detail = Profile.confirm(**ser_data.data)
        return Response({'detail': detail}, status=status)

    
class LoginViewSet(viewsets.ViewSet):

    def create(self, request):
        ser_data = LoginSerializer(data=request.data)
        ser_data.is_valid(raise_exception=True)
        user = get_object_or_404(Profile, username=ser_data.data['username'])
        status, detail = user.login(ser_data.data['password'])
        return Response({'detail': detail}, status=status)


class UserInfoViewSet(mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        viewsets.GenericViewSet):

    serializer_class = EditProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, username=self.request.user)
        return obj


class LogoutViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        ser_data = LogoutSerializer(data=request.data)
        ser_data.is_valid(raise_exception=True)
        refresh = ser_data.data['refresh']
        user = request.user
        status, detail = user.logout(refresh)
        return Response({'detail': detail}, status=status)


class ChangePasswordViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def partial_update(self, request, pk=None):
        ser_data = ChangePasswordSerializer(
            data=request.data, context={'request': request})
        ser_data.is_valid(raise_exception=True)
        new_password = ser_data.data['new_password']
        user = request.user
        status, detail = user.change_password(new_password)
        return Response({'detail': detail}, status=status)
