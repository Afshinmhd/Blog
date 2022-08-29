from rest_framework import viewsets, mixins
from .serializers import RegisterSerializer
from django.contrib.auth.models import User


class RegisterViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
        This class used to create user
    """

    serializer_class = RegisterSerializer
    # queryset = User.objects.all()

    # def perform_create(self, serializer):
    #     del serializer['password2']
    #     serializer.save()


    
