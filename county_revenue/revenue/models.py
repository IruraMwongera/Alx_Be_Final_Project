from django.db import models
from decimal import Decimal
from django.conf import settings
from django.contrib.auth.models import User
import uuid
class Permit(models.Model):
    PERMIT_TYPES = [('single_business','Single Business Permit'),('building','Building Permit'),('liquor','Liquor License'),('advert','Advertisement Permit'),('env_health','Environmental/Health Permit')]
    STATUS = [('pending','Pending'),('approved','Approved'),('rejected','Rejected'),('expired','Expired')]
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='permits')
    permit_type = models.CharField(max_length=50, choices=PERMIT_TYPES)
    data = models.JSONField(default=dict, blank=True)
    fee = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    valid_from = models.DateField(null=True, blank=True)
    valid_to = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    qr_code = models.ImageField(upload_to='qrcodes/', null=True, blank=True)
    pdf_file = models.FileField(upload_to='permits/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.permit_type} - {self.uid}"
class Transaction(models.Model):
    STATUS = [('pending','Pending'),('success','Success'),('failed','Failed'),('refunded','Refunded')]
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transactions')
    permit = models.ForeignKey(Permit, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    method = models.CharField(max_length=50)
    reference = models.CharField(max_length=128, unique=True)
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.reference} - {self.amount} ({self.status})"
class Property(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='properties')
    lr_number = models.CharField(max_length=128)
    location = models.CharField(max_length=255)
    valuation = models.DecimalField(max_digits=14, decimal_places=2)
    arrears = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    def __str__(self):
        return f"{self.lr_number} - {self.location}"
# ------------------------------
# Town
# ------------------------------
class Town(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# ------------------------------
# Area within a town
# ------------------------------
class Area(models.Model):
    town = models.ForeignKey(Town, on_delete=models.CASCADE, related_name="areas")
    name = models.CharField(max_length=100)  # e.g., Makutano

    def __str__(self):
        return f"{self.town.name} - {self.name}"

# ------------------------------
# Parking Section within an area
# ------------------------------
class ParkingSection(models.Model):
    area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name="sections")
    name = models.CharField(max_length=50)  # "1", "2", "3", "Others"
    capacity = models.PositiveIntegerField(default=1)
    is_custom = models.BooleanField(default=False)  # True if 'Others' section

    def __str__(self):
        return f"{self.area.name} - {self.name}"

# ------------------------------
# Vehicle
# ------------------------------
class Vehicle(models.Model):
    VEHICLE_CHOICES = [
        ("saloon", "Saloon Car"),
        ("van", "Van"),
        ("bus_lorry", "Bus / Small Lorry"),
        ("truck_tanker", "Truck / Tanker"),
    ]
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="vehicles")
    plate_number = models.CharField(max_length=20)
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_CHOICES)

    def __str__(self):
        return f"{self.plate_number} ({self.get_vehicle_type_display()})"

# ------------------------------
# Parking Ticket
# ------------------------------
class ParkingTicket(models.Model):
    TIME_UNIT_CHOICES = [
        ("minutes", "Minutes"),
        ("hours", "Hours"),
        ("days", "Days"),
    ]

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    section = models.ForeignKey(ParkingSection, on_delete=models.CASCADE)
    custom_place = models.CharField(max_length=255, blank=True, null=True)
    duration = models.PositiveIntegerField()
    time_unit = models.CharField(max_length=10, choices=TIME_UNIT_CHOICES)

    amount = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    paid = models.BooleanField(default=False)

    # Self-contained fields
    plate_number = models.CharField(max_length=20)
    vehicle_type = models.CharField(max_length=20)
    town_name = models.CharField(max_length=100, blank=True, null=True)
    area_name = models.CharField(max_length=100, blank=True, null=True)

    def calculate_amount(self):
        VEHICLE_RATES = {
            "saloon": Decimal("300"),
            "van": Decimal("500"),
            "bus_lorry": Decimal("700"),
            "truck_tanker": Decimal("900"),
        }
        rate = VEHICLE_RATES.get(self.vehicle.vehicle_type, Decimal(0))
        if self.time_unit == "minutes":
            return rate / Decimal(24 * 60) * Decimal(self.duration)
        elif self.time_unit == "hours":
            return rate / Decimal(24) * Decimal(self.duration)
        elif self.time_unit == "days":
            return rate * Decimal(self.duration)
        return Decimal(0)

    def save(self, *args, **kwargs):
        self.amount = self.calculate_amount()

        # Save vehicle & section info on ticket
        if self.vehicle:
            self.plate_number = self.vehicle.plate_number
            self.vehicle_type = self.vehicle.vehicle_type
        if self.section:
            self.town_name = self.section.area.town.name
            self.area_name = self.section.area.name

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.plate_number} - {self.section.name} ({self.duration} {self.time_unit})"
class MarketStall(models.Model):
    trader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    market_name = models.CharField(max_length=100)
    stall_number = models.CharField(max_length=50)
    monthly_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
class Advertisement(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    advert_type = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    duration_days = models.IntegerField(default=30)
    fee = models.DecimalField(max_digits=12, decimal_places=2)
class BuildingProject(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan_doc = models.FileField(upload_to='plans/')
    status = models.CharField(max_length=50, default='pending')
    fee = models.DecimalField(max_digits=12, decimal_places=2, default=0)
class AuditLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    action = models.TextField()
    ip_address = models.CharField(max_length=50, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
