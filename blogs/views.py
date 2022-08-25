from rest_framework import viewsets
from .serializers import ArticleSerializer
from .models import ArticleModel
from .permissions import IsOwnerOrReadOnly


class ArticleViewSet(viewsets.ModelViewSet):
    """
        This class used to create article
    """

    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = ArticleSerializer
    queryset = ArticleModel.objects.all()
