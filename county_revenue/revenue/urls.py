from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PermitViewSet, TransactionViewSet, PropertyViewSet, ParkingZoneViewSet,
    ParkingTicketViewSet, MarketStallViewSet, AdvertisementViewSet,
    BuildingProjectViewSet, AuditLogViewSet
)

router = DefaultRouter()
router.register(r'permits', PermitViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'properties', PropertyViewSet)
router.register(r'parkingzones', ParkingZoneViewSet)
router.register(r'parkingtickets', ParkingTicketViewSet)
router.register(r'marketstalls', MarketStallViewSet)
router.register(r'advertisements', AdvertisementViewSet)
router.register(r'buildingprojects', BuildingProjectViewSet)
router.register(r'auditlogs', AuditLogViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
