from django import forms
from parking.models import VehicleCategory, VehicleRegistration

class VehicleCategoryForm(forms.ModelForm):
    class Meta:
        model = VehicleCategory
        fields = '__all__'


class VehicleRegistrationForm(forms.ModelForm):
    class Meta:
        model = VehicleRegistration
        fields = [
            'type', 'driver_name', 'number_plate', 'model',
            'color', 'phone_number', 'nin',
            'rate', 'status'
        ]

        