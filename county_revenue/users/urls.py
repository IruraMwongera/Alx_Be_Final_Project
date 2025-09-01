from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, RegisterAPIView, LoginAPIView, LogoutAPIView, ProfileAPIView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path("api/register/", RegisterAPIView.as_view(), name="api-register"),
    path("api/login/", LoginAPIView.as_view(), name="api-login"),
    path("api/logout/", LogoutAPIView.as_view(), name="api-logout"),
    path("api/profile/", ProfileAPIView.as_view(), name="api-profile"),
    path("api/", include(router.urls)),
]
