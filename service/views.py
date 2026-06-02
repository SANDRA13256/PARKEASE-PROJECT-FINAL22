from django.shortcuts import render, redirect, get_object_or_404
from .models import ServicePrice, TyreService, BatteryService
from .forms import ServicePriceForm, TyreServiceForm, BatteryServiceForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum

# SERVICE PRICE VIEWS

def serviceprice_list(request):
    prices = ServicePrice.objects.all()
    return render(request, 'serviceprice_list.html', {'prices': prices})


def add_serviceprice(request):
    form = ServicePriceForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('service:serviceprice_list')

    return render(request, 'serviceprice_form.html', {'form': form})


def update_serviceprice(request, pk):
    price = get_object_or_404(ServicePrice, pk=pk)
    form = ServicePriceForm(request.POST or None, instance=price)

    if form.is_valid():
        form.save()
        return redirect('service:serviceprice_list')
    return render(request, 'serviceprice_form.html', {'form': form})


def delete_serviceprice(request, pk):
    price = get_object_or_404(ServicePrice, pk=pk)

    if request.method == 'POST':
        price.delete()
        return redirect('service:serviceprice_list')

    return render(request, 'confirm_delete.html', {'object': price})


# TYRE SERVICE VIEWS

@login_required
def tyre_list(request):
    if request.user.role != 'MANAGER':
        return redirect('accounts:login')

    query = request.GET.get('q')
    tyres = TyreService.objects.all()

    if query:
        tyres = tyres.filter(vehicle_plate__icontains=query)

    return render(request, 'tyre_list.html', {'tyres': tyres})

def add_tyre(request):
    form = TyreServiceForm(request.POST or None)

    if form.is_valid():
        form.save()

        return redirect('service:tyre_list')
    return render(request, 'tyre_form.html', {'form': form})


def delete_tyre(request, pk):
    tyre = get_object_or_404(TyreService, pk=pk)

    if request.method == 'POST':
        tyre.delete()
        return redirect('service:tyre_list')
    

    return render(request, 'confirm_delete.html', {'object': tyre})

# BATTERY SERVICE VIEWS
@login_required
def battery_list(request):

    if not hasattr(request.user, 'role') or request.user.role != 'MANAGER':
        return redirect('accounts:login')

    batteries = BatteryService.objects.all().order_by('-date')

    return render(request, 'battery_list.html', {'batteries': batteries})
@login_required
def add_battery(request):

    if not hasattr(request.user, 'role') or request.user.role != 'MANAGER':
        return redirect('accounts:login')

    form = BatteryServiceForm(request.POST or None)

    if form.is_valid():
        battery = form.save()

        return redirect('service:battery_receipt', pk=battery.id)

    return render(request, 'battery_form.html', {'form': form})

def delete_battery(request, pk):
    battery = get_object_or_404(BatteryService, pk=pk)

    if request.method == 'POST':
        battery.delete()
        return redirect('service:battery_list')

    return render(request, 'confirm_delete.html', {'object': battery})

@login_required
def manager_dashboard(request):
    if request.user.role != 'MANAGER':
        return redirect('accounts:login')

    today = timezone.now().date()

    # TYRE
    tyre_today = TyreService.objects.filter(date__date=today)
    tyre_total = tyre_today.aggregate(total=Sum('price'))['total'] or 0

    # BATTERY
    battery_today = BatteryService.objects.filter(date__date=today)
    battery_total = battery_today.aggregate(total=Sum('price'))['total'] or 0

    # TOTAL
    total_revenue = tyre_total + battery_total

    context = {
        'tyre_total': tyre_total,
        'battery_total': battery_total,
        'total_revenue': total_revenue,
        'tyre_count': tyre_today.count(),
        'battery_count': battery_today.count(),
    }

    return render(request, 'manager_dashboard.html', context)


def tyre_receipt(request, pk):
    tyre = get_object_or_404(TyreService, pk=pk)
    return render(request, 'tyre_receipt.html', {'tyre': tyre})


def battery_receipt(request, pk):
    battery = get_object_or_404(BatteryService, pk=pk)
    return render(request, 'battery_receipt.html', {'battery': battery})

@login_required
def service_dashboard(request):
    today = timezone.now().date()

    tyres_today = TyreService.objects.filter(date__date=today)
    batteries_today = BatteryService.objects.filter(date__date=today)

    tyre_total = tyres_today.aggregate(total=Sum('price'))['total'] or 0
    battery_total = batteries_today.aggregate(total=Sum('price'))['total'] or 0

    context = {
        'tyres': TyreService.objects.all().order_by('-date'),
        'batteries': BatteryService.objects.all().order_by('-date'),
        'tyre_total': tyre_total,
        'battery_total': battery_total,
        'total_revenue': tyre_total + battery_total,
    }

    return render(request, 'service_dashboard.html', context)
