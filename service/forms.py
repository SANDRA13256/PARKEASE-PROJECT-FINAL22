from django import forms
from .models import ServicePrice, TyreService, BatteryService


class ServicePriceForm(forms.ModelForm):
    class Meta:
        model = ServicePrice
        fields = "__all__"

class TyreServiceForm(forms.ModelForm):
    class Meta:
        model = TyreService
        fields = ["vehicle_plate", "service"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['service'].queryset = ServicePrice.objects.filter(category='tyre')

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class BatteryServiceForm(forms.ModelForm):
    class Meta:
        model = BatteryService
        fields = ["customer_name", "service"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['service'].queryset = ServicePrice.objects.filter(category='battery')

        # ADD STYLING
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})