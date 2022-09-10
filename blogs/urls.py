from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet, CommentViewSet


router = DefaultRouter()
router.register(r'article', ArticleViewSet, basename='article')
router.register(r'comment', ArticleViewSet, basename='comment')
urlpatterns = router.urls