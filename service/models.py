from django.db import models
import uuid
from django.db import models

class ServicePrice(models.Model):

    CATEGORY_CHOICES = [
        ('tyre', 'Tyre'),
        ('battery', 'Battery'),
    ]

    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='tyre')

    SERVICE_TYPES = [
        ("pressure", "Tyre Pressure"),
        ("puncture", "Puncture Fixing"),
        ("valve", "Valve Replacement"),
        ("battery_hire", "Battery Hire"),
        ("battery_sale", "Battery Sale"),
    ]

    name = models.CharField(max_length=20, choices=SERVICE_TYPES)
    vehicle_size = models.CharField(max_length=50, null=True, blank=True)
    model = models.CharField(max_length=50, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.get_name_display()} - UGX {self.price}"
    
class TyreService(models.Model):
    vehicle_plate = models.CharField(max_length=10)
    service = models.ForeignKey(ServicePrice, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    receipt_number = models.CharField(max_length=20, unique=True, editable=False)
    date = models.DateTimeField(auto_now_add=True)
    

    def save(self, *args, **kwargs):
        if not self.receipt_number:
            self.receipt_number = f"TYR-{uuid.uuid4().hex[:6].upper()}"

        if self.service:
            self.price = self.service.price

        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.vehicle_plate} - {self.service.name}"


class BatteryService(models.Model):

    customer_name = models.CharField(max_length=100)

    
    service = models.ForeignKey(ServicePrice, on_delete=models.CASCADE)

    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    receipt_number = models.CharField(max_length=20, unique=True, editable=False)
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.receipt_number:
            self.receipt_number = f"BAT-{uuid.uuid4().hex[:6].upper()}"

        # Automated prices from service
        if self.service:
            self.price = self.service.price

        super().save(*args, **kwargs)
        def __str__(self):
          return f"{self.get_name_display()} - UGX {self.price}"