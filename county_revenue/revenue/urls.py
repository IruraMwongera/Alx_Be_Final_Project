# revenue/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PermitViewSet,
    ParkingTicketViewSet,
    TownListAPIView,
    AreaByTownAPIView,
    ParkingSectionByAreaAPIView,
)

# Router for ViewSets
router = DefaultRouter()
router.register(r'permits', PermitViewSet, basename='permit')
router.register(r'tickets', ParkingTicketViewSet, basename='ticket')

urlpatterns = [
    # ViewSets (CRUD + custom actions)
    path("", include(router.urls)),

    # Towns, Areas, Sections
    path("towns/", TownListAPIView.as_view(), name="town-list"),
    path("towns/<int:town_id>/areas/", AreaByTownAPIView.as_view(), name="areas-by-town"),
    path("areas/<int:area_id>/sections/", ParkingSectionByAreaAPIView.as_view(), name="sections-by-area"),
]
