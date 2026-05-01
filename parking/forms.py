from django import forms
from parking.models import VehicleCategory, VehicleRegistration
import re


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

    #  Driver Name Validation
    def clean_driver_name(self):
        name = self.cleaned_data.get('driver_name')

        if name:
            if not name[0].isupper():
                raise forms.ValidationError("Name must start with a capital letter")

            if any(char.isdigit() for char in name):
                raise forms.ValidationError("Name must not contain numbers")

        return name

    #  Number Plate Validation
    def clean_number_plate(self):
        plate = self.cleaned_data.get('number_plate')

        if not plate:
            raise forms.ValidationError("Number plate is required")

        plate = plate.upper()

        if not plate.startswith('U'):
            raise forms.ValidationError("Plate must start with 'U'")

        if not plate.isalnum():
            raise forms.ValidationError("Plate must be alphanumeric")

        if len(plate) > 6:
            raise forms.ValidationError("Plate must not exceed 6 characters")

        return plate

    #  Phone Number Validation (UGANDA)
    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')

        if not phone.isdigit():
            raise forms.ValidationError("Phone must contain digits only")

        # Uganda formats
        if not (re.match(r'^07\d{8}$', phone) or re.match(r'^2567\d{8}$', phone)):
            raise forms.ValidationError("Enter a valid Ugandan phone number")

        return phone

    # ID NIN Validation
    def clean_nin(self):
        nin = self.cleaned_data.get('nin')

        if not re.match(r'^[A-Z]{2}\d{8}[A-Z]{3}$', nin):
            raise forms.ValidationError("Enter a valid NIN (e.g. CM12345678ABC)")

        return nin.upper()

    # This is to prevent duplicate of parked vehicles
    def clean(self):
        cleaned_data = super().clean()
        plate = cleaned_data.get('number_plate')
        status = cleaned_data.get('status')

        if plate and status == 'parked':
            exists = VehicleRegistration.objects.filter(
                number_plate=plate,
                status='parked'
            ).exclude(pk=self.instance.pk).exists()

            if exists:
                raise forms.ValidationError("This vehicle is already parked")

        return cleaned_data