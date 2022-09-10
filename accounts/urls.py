from rest_framework.routers import DefaultRouter
from .views import (UserInfoViewSet, LoginViewSet,
                    ConfirmViewSet, SubLoginViewSet,
                    ChangePasswordViewSet,LogoutViewSet)


router = DefaultRouter()
router.register(r'login', LoginViewSet, basename='login')
router.register(r'sub_login', SubLoginViewSet, basename='sub_login')
router.register(r'confirm', ConfirmViewSet, basename='confirm')
router.register(r'edit_user', UserInfoViewSet, basename='edit_user')
router.register(r'change_password', ChangePasswordViewSet, basename='change_password')
router.register(r'Logout', LoginViewSet, basename='Logout')
urlpatterns = router.urls