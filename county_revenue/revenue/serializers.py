# revenue/serializers.py
from rest_framework import serializers
from .models import (
    Permit, PermitType, ParkingSection, ParkingTicket,
    Vehicle, Town, Area
)

# ------------------------------
# PERMIT TYPE
# ------------------------------
class PermitTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermitType
        fields = "__all__"

# ------------------------------
# PERMIT
# ------------------------------
class PermitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permit
        fields = "__all__"
        read_only_fields = [
            "owner",
            "owner_name",
            "permit_number",
            "start_date",
            "end_date",
            "total_fee",
            "paid",
        ]

# ------------------------------
# TOWNS / AREAS / PARKING SECTIONS
# ------------------------------
class TownSerializer(serializers.ModelSerializer):
    class Meta:
        model = Town
        fields = "__all__"

class AreaSerializer(serializers.ModelSerializer):
    town = TownSerializer(read_only=True)

    class Meta:
        model = Area
        fields = "__all__"

class ParkingSectionSerializer(serializers.ModelSerializer):
    area = AreaSerializer(read_only=True)

    class Meta:
        model = ParkingSection
        fields = "__all__"

# ------------------------------
# VEHICLE (for tickets)
# ------------------------------
class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = "__all__"
        read_only_fields = ["owner"]

# ------------------------------
# PARKING TICKET
# ------------------------------
class ParkingTicketSerializer(serializers.ModelSerializer):
    vehicle = VehicleSerializer(read_only=True)
    town_name = serializers.CharField(read_only=True)
    area_name = serializers.CharField(read_only=True)

    class Meta:
        model = ParkingTicket
        fields = "__all__"
        read_only_fields = [
            "town_name",
            "area_name",
            "vehicle",
            "vehicle_type",
            "plate_number",  # derived from vehicle
        ]
