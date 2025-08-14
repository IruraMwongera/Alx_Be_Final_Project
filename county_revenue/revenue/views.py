from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Permit
from .serializers import PermitSerializer
from django.shortcuts import render
from .models import (
    Permit, Transaction, Property, ParkingZone, ParkingTicket,
    MarketStall, Advertisement, BuildingProject, AuditLog
)
from .serializers import (
    PermitSerializer, TransactionSerializer, PropertySerializer,
    ParkingZoneSerializer, ParkingTicketSerializer, MarketStallSerializer,
    AdvertisementSerializer, BuildingProjectSerializer, AuditLogSerializer
)

# Permit ViewSet
class PermitViewSet(viewsets.ModelViewSet):
    queryset = Permit.objects.all()
    serializer_class = PermitSerializer
    permission_classes = [permissions.IsAuthenticated]

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

# ParkingZone ViewSet
class ParkingZoneViewSet(viewsets.ModelViewSet):
    queryset = ParkingZone.objects.all()
    serializer_class = ParkingZoneSerializer
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

# AuditLog ViewSet
class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAdminUser]

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

