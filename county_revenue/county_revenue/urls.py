from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from revenue.views import PermitViewSet, PermitTypeViewSet
from users.views import UserViewSet

# ------------------------------
# DRF router
# ------------------------------
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'permits', PermitViewSet, basename='permit')
router.register(r'permit-types', PermitTypeViewSet, basename='permittype')  # Added

urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),

    # API routes
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),  # DRF login/logout

    # Token login
    path('api/login/', obtain_auth_token, name='api_login'),

    # App routes (if you have app-level urls.py)
    path('users/', include('users.urls')),
    path('revenue/', include('revenue.urls')),
]
