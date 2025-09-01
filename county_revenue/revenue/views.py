# revenue/views.py

from rest_framework import viewsets, permissions, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa

from .models import (
    Permit, PermitType, ParkingSection, ParkingTicket,
    Vehicle, Town, Area
)
from .serializers import (
    PermitSerializer, PermitTypeSerializer, ParkingTicketSerializer,
    ParkingSectionSerializer, TownSerializer, AreaSerializer
)

# ------------------------------
# PERMIT TYPE API
# ------------------------------
class PermitTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only API for permit types"""
    queryset = PermitType.objects.all()
    serializer_class = PermitTypeSerializer
    permission_classes = [permissions.AllowAny]


# ------------------------------
# PERMIT API
# ------------------------------
class PermitViewSet(viewsets.ModelViewSet):
    queryset = Permit.objects.all()
    serializer_class = PermitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        permit = serializer.save(
            owner=self.request.user,
            owner_name=self.request.user.get_full_name() or self.request.user.username
        )
        permit_type = permit.permit_type

        # Handle duration logic
        if permit_type.is_monthly:
            permit.duration_months = permit.duration_months or 1
            permit.duration_days = None
        elif permit_type.is_daily:
            permit.duration_days = permit.duration_days or 1
            permit.duration_months = None
        elif permit_type.is_yearly:
            permit.duration_years = permit.duration_years or 1
            permit.duration_days = None
            permit.duration_months = None

        permit.save()

    def get_queryset(self):
        if self.request.user.is_staff:
            return Permit.objects.all()
        return Permit.objects.filter(owner=self.request.user)

    @action(detail=True, methods=['get'])
    def pdf(self, request, pk=None):
        """Generate Permit PDF"""
        permit = get_object_or_404(Permit, pk=pk, owner=request.user)
        template_path = "revenue/permit/permit_pdf.html"
        context = {
            "permit": permit,
            "permit_type_display": permit.permit_type.name,
            "start_date_display": permit.start_date.strftime("%b %d, %Y") if permit.start_date else "",
            "end_date_display": permit.end_date.strftime("%b %d, %Y") if permit.end_date else "",
        }
        html = render_to_string(template_path, context)
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="permit_{permit.id}.pdf"'
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse("Error generating PDF")
        return response


# ------------------------------
# PARKING TICKET API
# ------------------------------
class ParkingTicketViewSet(viewsets.ModelViewSet):
    queryset = ParkingTicket.objects.all()
    serializer_class = ParkingTicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        section = serializer.validated_data["section"]
        area = section.area
        town = area.town

        vehicle, created = Vehicle.objects.get_or_create(
            owner=self.request.user,
            plate_number=serializer.validated_data["plate_number"],
            defaults={"vehicle_type": serializer.validated_data["vehicle_type"]}
        )

        serializer.save(
            section=section,
            town_name=town.name,
            area_name=area.name,
            vehicle=vehicle,
            vehicle_type=vehicle.vehicle_type,
            plate_number=vehicle.plate_number
        )

    def get_queryset(self):
        if self.request.user.is_staff:
            return ParkingTicket.objects.all()
        return ParkingTicket.objects.filter(vehicle__owner=self.request.user)

    @action(detail=True, methods=['get'])
    def pdf(self, request, pk=None):
        """Generate Ticket PDF"""
        ticket = get_object_or_404(ParkingTicket, pk=pk, vehicle__owner=request.user)
        template_path = "revenue/parking/ticket_pdf.html"
        context = {"ticket": ticket}
        html = render_to_string(template_path, context)
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="ticket_{ticket.id}.pdf"'
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse("Error generating PDF")
        return response


# ------------------------------
# TOWNS / AREAS / PARKING ZONES
# ------------------------------
class TownListAPIView(generics.ListAPIView):
    queryset = Town.objects.all()
    serializer_class = TownSerializer
    permission_classes = [permissions.AllowAny]


class AreaByTownAPIView(generics.ListAPIView):
    serializer_class = AreaSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Area.objects.filter(town_id=self.kwargs["town_id"])


class ParkingSectionByAreaAPIView(generics.ListAPIView):
    serializer_class = ParkingSectionSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return ParkingSection.objects.filter(area_id=self.kwargs["area_id"])
