from rest_framework import viewsets
from .serializers import ArticleSerializer
from .models import ArticleModel
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import AllowAny


class ArticleViewSet(viewsets.ModelViewSet):
    """
        This class used to create article
    """

    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = ArticleSerializer
    queryset = ArticleModel.objects.all()


    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
