
from django.http import JsonResponse
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    Permit, Transaction, Property, ParkingTicket,ParkingSection,Area,
   MarketStall, Advertisement, BuildingProject, AuditLog
)
from .serializers import (
    PermitSerializer, TransactionSerializer, PropertySerializer,  ParkingTicketSerializer, MarketStallSerializer,
    AdvertisementSerializer, BuildingProjectSerializer, AuditLogSerializer,ParkingSectionSerializer
)

# Permit ViewSet
class PermitViewSet(viewsets.ModelViewSet):
    queryset = Permit.objects.all()
    serializer_class = PermitSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'permit_type']
    search_fields = ['uid']
    ordering_fields = ['created_at', 'valid_to']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# Transaction ViewSet
class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# Property ViewSet
class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
class ParkingSectionViewSet(viewsets.ModelViewSet):
    queryset = ParkingSection.objects.all()
    serializer_class = ParkingSectionSerializer
    permission_classes = [permissions.IsAuthenticated]
# ParkingTicket ViewSet
class ParkingTicketViewSet(viewsets.ModelViewSet):
    queryset = ParkingTicket.objects.all()
    serializer_class = ParkingTicketSerializer
    permission_classes = [permissions.IsAuthenticated]

# MarketStall ViewSet
class MarketStallViewSet(viewsets.ModelViewSet):
    queryset = MarketStall.objects.all()
    serializer_class = MarketStallSerializer
    permission_classes = [permissions.IsAuthenticated]

# Advertisement ViewSet
class AdvertisementViewSet(viewsets.ModelViewSet):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [permissions.IsAuthenticated]

# BuildingProject ViewSet
class BuildingProjectViewSet(viewsets.ModelViewSet):
    queryset = BuildingProject.objects.all()
    serializer_class = BuildingProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

# AuditLog ViewSet (Read Only for Admins)
class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAdminUser]
def load_areas(request):
    town_id = request.GET.get("town")
    areas = Area.objects.filter(town_id=town_id).values("id", "name")
    return JsonResponse(list(areas), safe=False)

def load_sections(request):
    area_id = request.GET.get("area")
    sections = ParkingSection.objects.filter(area_id=area_id).values("id", "name")
    return JsonResponse(list(sections), safe=False)

