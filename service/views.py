from django.shortcuts import render, redirect, get_object_or_404
from .models import ServicePrice, TyreService, BatteryService
from .forms import ServicePriceForm, TyreServiceForm, BatteryServiceForm


# ======================================
# SERVICE PRICE VIEWS
# ======================================

def serviceprice_list(request):
    prices = ServicePrice.objects.all()
    return render(request, 'serviceprice_list.html', {'prices': prices})


def add_serviceprice(request):
    form = ServicePriceForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('serviceprice_list')

    return render(request, 'serviceprice_form.html', {'form': form})


def update_serviceprice(request, pk):
    price = get_object_or_404(ServicePrice, pk=pk)
    form = ServicePriceForm(request.POST or None, instance=price)

    if form.is_valid():
        form.save()
        return redirect('serviceprice_list')

    return render(request, 'serviceprice_form.html', {'form': form})


def delete_serviceprice(request, pk):
    price = get_object_or_404(ServicePrice, pk=pk)

    if request.method == 'POST':
        price.delete()
        return redirect('serviceprice_list')

    return render(request, 'confirm_delete.html', {'object': price})


# ======================================
# TYRE SERVICE VIEWS
# ======================================

def tyre_list(request):
    tyres = TyreService.objects.all()
    return render(request, 'tyre_list.html', {'tyres': tyres})


def add_tyre(request):
    form = TyreServiceForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('tyre_list')

    return render(request, 'tyre_form.html', {'form': form})


def delete_tyre(request, pk):
    tyre = get_object_or_404(TyreService, pk=pk)

    if request.method == 'POST':
        tyre.delete()
        return redirect('tyre_list')

    return render(request, 'confirm_delete.html', {'object': tyre})


# ======================================
# BATTERY SERVICE VIEWS
# ======================================

def battery_list(request):
    batteries = BatteryService.objects.all()
    return render(request, 'battery_list.html', {'batteries': batteries})


def add_battery(request):
    form = BatteryServiceForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('service:battery_list')

    return render(request, 'battery_form.html', {'form': form})


def delete_battery(request, pk):
    battery = get_object_or_404(BatteryService, pk=pk)

    if request.method == 'POST':
        battery.delete()
        return redirect('service:battery_list')

    return render(request, 'confirm_delete.html', {'object': battery})
from django.contrib.auth.decorators import login_required
from .models import TyreService, BatteryService

@login_required
def tyre_list(request):
    if request.user.role != 'MANAGER':
        return redirect('accounts:login')

    tyres = TyreService.objects.all()
    batteries = BatteryService.objects.all()

    return render(request, 'tyre_list.html', {
        'tyres': tyres,
        'batteries': batteries
    })
