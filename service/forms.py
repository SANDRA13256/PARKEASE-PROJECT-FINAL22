from django import forms
from .models import ServicePrice, TyreService, BatteryService


class ServicePriceForm(forms.ModelForm):
    class Meta:
        model = ServicePrice
        fields = "__all__"

class TyreServiceForm(forms.ModelForm):
    class Meta:
        model = TyreService
        fields = [
            "vehicle_plate",
            "service",
            
        ]

class BatteryServiceForm(forms.ModelForm):
    class Meta:
        model = BatteryService
        fields = [
            "customer_name",
            "battery_type",
            "price",
        ]