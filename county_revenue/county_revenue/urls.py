from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from revenue.views_html import PermitViewSet, home_view
from users.views import UserViewSet  # Make sure this exists

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'permits', PermitViewSet)

urlpatterns = [
    path('', home_view, name='home'),


    # Django admin
    path('admin/', admin.site.urls),

    # API routes
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),  # DRF login/logout

    # HTML routes
    path('users/', include('users.urls')),      # Users app HTML
    path('revenue/', include('revenue.urls')),  # Revenue app HTML
]
