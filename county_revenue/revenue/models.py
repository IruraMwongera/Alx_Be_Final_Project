from django.db import models
from decimal import Decimal
from datetime import date, timedelta
import uuid
from django.conf import settings
from decimal import Decimal, ROUND_HALF_UP
# ------------------------------
# Permit Type
# ------------------------------
class PermitType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    registration_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    annual_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Yearly permits
    monthly_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0) # Monthly permits (Hawking)
    daily_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)   # Daily permits (Special Events)
    is_yearly = models.BooleanField(default=False)
    is_monthly = models.BooleanField(default=False)
    is_daily = models.BooleanField(default=False)

    def __str__(self):
        return self.name


# ------------------------------
# Permit
# ------------------------------
class Permit(models.Model):
    permit_type = models.ForeignKey(PermitType, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    owner_name = models.CharField(max_length=200)
    permit_number = models.CharField(max_length=20, unique=True, blank=True)
    start_date = models.DateField(default=date.today)
    end_date = models.DateField(editable=False)
    renewed = models.BooleanField(default=False)

    # For daily permits (Alcohol Special Events)
    duration_days = models.PositiveIntegerField(default=1, blank=True, null=True)

    # For monthly permits (Hawking)
    duration_months = models.PositiveIntegerField(default=1, blank=True, null=True)

    # Fees and payment tracking
    total_fee = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=0)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    paid = models.BooleanField(default=False)

    notes = models.TextField(blank=True, null=True)

    def calculate_fee(self):
        """
        Calculates the total fee based on permit type.
        """
        # Yearly permits
        if self.permit_type.is_yearly:
            remaining_months = 12 - self.start_date.month + 1
            monthly_portion = self.permit_type.annual_fee / 12
            return self.permit_type.registration_fee + (monthly_portion * remaining_months)

        # Monthly permits (Hawking, capped at 2400)
        elif self.permit_type.is_monthly:
            months = self.duration_months or 1
            fee = self.permit_type.monthly_fee * months
            return min(fee, Decimal(2400))

        # Daily permits (Alcohol Special Event)
        elif self.permit_type.is_daily:
            days = self.duration_days or 1
            return self.permit_type.daily_fee * days

        return Decimal(0)

    def save(self, *args, **kwargs):
        # Assign unique permit number if not already assigned
        if not self.permit_number:
            self.permit_number = str(uuid.uuid4()).split('-')[0].upper()

        # Calculate total fee
        self.total_fee = self.calculate_fee()

        # Set end_date based on permit type
        if self.permit_type.is_yearly:
            self.end_date = date(self.start_date.year, 12, 31)
        elif self.permit_type.is_monthly:
            months = self.duration_months or 1
            self.end_date = self.start_date + timedelta(days=30 * months - 1)
        elif self.permit_type.is_daily:
            days = self.duration_days or 1
            self.end_date = self.start_date + timedelta(days=days - 1)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.owner_name} - {self.permit_type.name} ({self.permit_number})"


# ------------------------------
# Prepopulate Permit Types
# ------------------------------
def create_permit_types():
    permit_data = [
        {"name": "Large Business", "annual_fee": 40000, "registration_fee": 3000, "is_yearly": True},
        {"name": "Small Business", "annual_fee": 12000, "registration_fee": 3000, "is_yearly": True},
        {"name": "Market Stall", "annual_fee": 17000, "registration_fee": 3000, "is_yearly": True},
        {"name": "Hawking", "monthly_fee": 200, "is_monthly": True},
        {"name": "Alcohol On-Sale", "annual_fee": 27000, "registration_fee": 3000, "is_yearly": True},
        {"name": "Alcohol Off-Sale", "annual_fee": 17000, "registration_fee": 3000, "is_yearly": True},
        {"name": "Alcohol Special Event", "daily_fee": 3000, "is_daily": True},
        {"name": "Night Club / Lounge", "annual_fee": 37000, "registration_fee": 3000, "is_yearly": True},
        {"name": "PSV", "annual_fee": 10000, "registration_fee": 3000, "is_yearly": True},
    ]

    for p in permit_data:
        PermitType.objects.update_or_create(name=p["name"], defaults=p)
# ------------------------------
# Town
# ------------------------------
class Town(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# ------------------------------
# Area
# ------------------------------
class Area(models.Model):
    town = models.ForeignKey(Town, on_delete=models.CASCADE, related_name="areas")
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.town.name} - {self.name}"

# ------------------------------
# Parking Section
# ------------------------------
class ParkingSection(models.Model):
    area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name="sections")
    name = models.CharField(max_length=50)
    capacity = models.PositiveIntegerField(default=1)
    is_custom = models.BooleanField(default=False)

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
    plate_number = models.CharField(max_length=40)
    vehicle_type = models.CharField(max_length=40, choices=VEHICLE_CHOICES)

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
    plate_number = models.CharField(max_length=40) 
    vehicle_type = models.CharField(max_length=40)
    town_name = models.CharField(max_length=100, blank=True, null=True)
    area_name = models.CharField(max_length=100, blank=True, null=True)

    # Add timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_amount(self):
        VEHICLE_RATES = {
            "saloon": Decimal("60"),
            "van": Decimal("100"),
            "bus_lorry": Decimal("140"),
            "truck_tanker": Decimal("180"),
        }
        rate = VEHICLE_RATES.get(self.vehicle.vehicle_type, Decimal(0))

        if self.time_unit == "minutes":
            amount = rate / Decimal(60) * Decimal(self.duration)
        elif self.time_unit == "hours":
            amount = rate * Decimal(self.duration)
        elif self.time_unit == "days":
            amount = rate * Decimal(24) * Decimal(self.duration)
        else:
            amount = Decimal(0)

        # Round to 2 decimal places
        return amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def save(self, *args, **kwargs):
        self.amount = self.calculate_amount()
        if self.vehicle:
            self.plate_number = self.vehicle.plate_number
            self.vehicle_type = self.vehicle.vehicle_type
        if self.section:
            self.town_name = self.section.area.town.name
            self.area_name = self.section.area.name
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.plate_number} - {self.section.name} ({self.duration} {self.time_unit})"
