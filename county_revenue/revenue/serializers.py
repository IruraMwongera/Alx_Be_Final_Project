from rest_framework import serializers
from .models import (
    Permit, Transaction, Property, ParkingSection, ParkingTicket,
    MarketStall, Advertisement, BuildingProject, AuditLog
)

class PermitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permit
        fields = '__all__'
        read_only_fields = ['owner', 'uid', 'created_at', 'updated_at']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ['owner', 'created_at']

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'
        read_only_fields = ['owner']

class ParkingSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingSection
        fields = '__all__'
class ParkingTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingTicket
        fields = '__all__'

class MarketStallSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketStall
        fields = '__all__'

class AdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = '__all__'
        read_only_fields = ['owner']

class BuildingProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildingProject
        fields = '__all__'
        read_only_fields = ['owner']

class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = '__all__'
        read_only_fields = ['user', 'timestamp']
