from rest_framework import viewsets, mixins
from .serializers import ArticleSerializer, CommentSerializer
from .models import ArticleModel, CommentModel
from .permissions import IsOwnerOrReadOnly, IsOwner
from rest_framework.permissions import AllowAny, IsAuthenticated


class ArticleViewSet(viewsets.ModelViewSet):
    """
        This class used to create article
    """

    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = ArticleSerializer
    queryset = ArticleModel.objects.all()


    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    """
        This class used to only create and delete comment
    """
    queryset = CommentModel.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated,]
        elif self.action == 'destroy':
            permission_classes = [IsOwner,]
        return[permission() for permission in permission_classes]
        
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)