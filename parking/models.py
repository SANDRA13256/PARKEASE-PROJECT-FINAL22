from django.db import models
import uuid
from django.utils import timezone
# Create your models here.

class VehicleCategory(models.Model):
    VEHICLE_TYPE =[ ('truck', 'Truck'), ('personal car', 'Personal Car'),('taxi', 'Taxi'),('coaster','Coaster'),('boda', 'boda boda')]
    vehicle_type =models.CharField(max_length=50, choices=VEHICLE_TYPE)
    day_rate = models.IntegerField()
    night_rate= models.IntegerField()
    short = models.IntegerField()

    def __str__(self):
        return self.vehicle_type

class VehicleRegistration(models.Model):
    RATE_TYPES = [('day','Day'), ('night','night'), ('short', 'Short')]
    STATUS_CHOICES =[('parked', 'Parked'), ('signed_out', 'Signed_Out')]

    type =models.ForeignKey(VehicleCategory, max_length=10, on_delete= models.CASCADE)
    driver_name = models.CharField(max_length=25, blank = True, null=True)
    number_plate =models.CharField(max_length=6, blank = True, null=True)
    model= models.CharField(max_length=25, blank = False, null=False)
    color=models.CharField(max_length=25, blank = True, null=True)
    phone_number=models.CharField(max_length=12, blank = False, null=False )
    nin=models.CharField(max_length=14, blank = False, null=False)
    arrival_time=models.DateTimeField(auto_now=True)
    receipt_number =models.CharField(max_length=20, unique=True, editable=False)
    rate = models.CharField(max_length=20, choices=RATE_TYPES, blank = True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank = False, null=False)
    departure_time = models.DateTimeField(blank=True, null = True, default= timezone.now)
    

    def save(self, *args, **kwargs):
     if not self.receipt_number:
        self.receipt_number = f'RPE-{uuid.uuid4().hex[:6].upper()}'
     super().save(*args, **kwargs)   

    def __str__(self):
     return f'{self.number_plate} ({self.receipt_number})'


