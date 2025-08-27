from rest_framework import serializers
from .models import Permit, ParkingSection, ParkingTicket

class PermitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permit
        fields = '__all__'
        read_only_fields = ['owner', 'uid', 'created_at', 'updated_at']

class ParkingSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingSection
        fields = '__all__'

class ParkingTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingTicket
        fields = '__all__'
