from django.db import models
from django.conf import settings
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
class ParkingZone(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    capacity = models.IntegerField(default=0)
    rate_per_hour = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    def __str__(self):
        return self.name
class ParkingTicket(models.Model):
    plate_number = models.CharField(max_length=20)
    zone = models.ForeignKey(ParkingZone, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)
    transaction = models.ForeignKey(Transaction, on_delete=models.SET_NULL, null=True, blank=True)
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
