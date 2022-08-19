from rest_framework import viewsets
from .serializers import RegisterSerializer
from django.contrib.auth.models import User


class RegisterViewSet(viewsets.ModelViewSet):
    """
        This class used to create user
    """

    serializer_class = RegisterSerializer
    queryset = User.objects.all()