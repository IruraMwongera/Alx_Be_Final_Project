from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet
from revenue.views import PermitViewSet, TransactionViewSet
from .views import home_view  # import home_view

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'permits', PermitViewSet)
router.register(r'transactions', TransactionViewSet)

urlpatterns = [
    path('', home_view, name='home'),

    # Django admin
    path('admin/', admin.site.urls),

    # API routes
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),  # DRF login/logout

    # HTML routes
    path('users/', include('users.urls')),              # HTML for users app
    path('revenue/', include('revenue.urls')),          # HTML for revenue app ✅
]
