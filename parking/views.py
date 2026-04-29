from django.shortcuts import render, redirect, get_object_or_404
from .forms import VehicleCategoryForm, VehicleRegistrationForm
from .models import VehicleCategory, VehicleRegistration
from django.utils import timezone
from django.contrib.auth.decorators import login_required


# Vehicle Category Views

def signout_vehicle(request, pk):
    vehicle = get_object_or_404(VehicleRegistration, pk=pk)

    vehicle.status = 'signed_out'
    vehicle.departure_time = timezone.now()
    vehicle.save()

    return redirect('parking:vehicle_list')


def category_list(request):
    categories = VehicleCategory.objects.all()
    return render(request, 'category_list.html', {'categories': categories})


def add_category(request):
    form = VehicleCategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('parking:category_list')

    return render(request, 'category_form.html', {'form': form})


# ---------------------------
# Vehicle Registration Views
# ---------------------------

def vehicle_list(request):
    vehicles = VehicleRegistration.objects.all()
    return render(request, 'vehicle_list.html', {'vehicles': vehicles})


def register_vehicle(request):
    form = VehicleRegistrationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('parking:vehicle_list')

    return render(request, 'vehicle_form.html', {'form': form})


def update_vehicle(request, pk):
    vehicle = get_object_or_404(VehicleRegistration, pk=pk)
    form = VehicleRegistrationForm(request.POST or None, instance=vehicle)

    if form.is_valid():
        form.save()
        return redirect('parking:vehicle_list')

    return render(request, 'vehicle_form.html', {'form': form})


def delete_vehicle(request, pk):
    vehicle = get_object_or_404(VehicleRegistration, pk=pk)

    if request.method == 'POST':
        vehicle.delete()
        return redirect('parking:vehicle_list')

    return render(request, 'confirm_delete.html', {'vehicle': vehicle})


def serviceprice_list(request):
    return render(request, 'parking/serviceprice_list.html')

    if form.is_valid():

     vehicle = form.save(commit=False)

     vehicle.status = 'parked'

     vehicle.save()
    return redirect('parking:vehicle_list')