from django.db import models
import uuid
from django.db import models

class ServicePrice(models.Model):

    SERVICE_TYPES = [
        ("pressure", "Tyre Pressure"),
        ("puncture", "Puncture Fixing"),
        ("valve", "Valve Replacement"),
    ]

    name = models.CharField(max_length=20, choices=SERVICE_TYPES)
    vehicle_size = models.CharField(max_length=50, null=True, blank=True)
    model = models.CharField(max_length=50, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} - UGX {self.price}"

class TyreService(models.Model):

    vehicle_plate = models.CharField(max_length=10)
    service = models.ForeignKey(ServicePrice, on_delete=models.CASCADE)
    receipt_number = models.CharField(max_length=20, unique=True, editable=False)
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.receipt_number:
            self.receipt_number = f"TYR-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.vehicle_plate} - {self.service.name}"


class BatteryService(models.Model):

    BATTERY_TYPES = [
        ("hire", "Battery Hire"),
        ("sale", "Battery Sale"),
    ]

    customer_name = models.CharField(max_length=100)
    battery_type = models.CharField(max_length=10, choices=BATTERY_TYPES)
    price = models.IntegerField()
    receipt_number = models.CharField(max_length=20, unique=True, editable=False)
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.receipt_number:
            self.receipt_number = f"BAT-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer_name} - {self.battery_type}"


