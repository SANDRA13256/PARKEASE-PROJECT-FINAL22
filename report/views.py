from django.db.models import Sum
from django.core.paginator import Paginator
from datetime import datetime, timedelta
from service.models import TyreService, BatteryService
from parking.models import VehicleRegistration
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone


@login_required
def admin_reports(request):

    if request.user.role != 'ADMIN':
        return redirect('accounts:login')

    # -----------------------------
    # DATE FILTER
    # -----------------------------
    date_str = request.GET.get('date')

    if date_str:
        selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    else:
        selected_date = timezone.now().date()

    previous_day = selected_date - timedelta(days=1)

    # -----------------------------
    # PARKING (SIGNED OUT ONLY)
    # -----------------------------
    vehicles = VehicleRegistration.objects.filter(
        status='signed_out',
        departure_time__date=selected_date
    )

    # -----------------------------
    # PARKING REVENUE (simple estimate)
    # -----------------------------
    parking_total = 0
    for v in vehicles:
        if v.rate == 'day':
            parking_total += v.type.day_rate
        elif v.rate == 'night':
            parking_total += v.type.night_rate
        elif v.rate == 'short':
            parking_total += v.type.short

    # -----------------------------
    # TYRE
    # -----------------------------
    tyre_today = TyreService.objects.filter(date__date=selected_date)
    tyre_total = tyre_today.aggregate(total=Sum('price'))['total'] or 0

    tyre_prev = TyreService.objects.filter(date__date=previous_day)\
        .aggregate(total=Sum('price'))['total'] or 0

    # -----------------------------
    # BATTERY
    # -----------------------------
    battery_today = BatteryService.objects.filter(date__date=selected_date)
    battery_total = battery_today.aggregate(total=Sum('price'))['total'] or 0

    battery_prev = BatteryService.objects.filter(date__date=previous_day)\
        .aggregate(total=Sum('price'))['total'] or 0

    # -----------------------------
    # PERCENTAGE CHANGE
    # -----------------------------
    def percent_change(today, prev):
        if prev == 0:
            return 100 if today > 0 else 0
        return round(((today - prev) / prev) * 100, 1)

    tyre_change = percent_change(tyre_total, tyre_prev)
    battery_change = percent_change(battery_total, battery_prev)

    # -----------------------------
    # SEARCH
    # -----------------------------
    query = request.GET.get('q')
    if query:
        vehicles = vehicles.filter(
            number_plate__icontains=query
        ) | vehicles.filter(
            receipt_number__icontains=query
        )

    # -----------------------------
    # PAGINATION
    # -----------------------------
    paginator = Paginator(vehicles.order_by('-departure_time'), 5)
    page = request.GET.get('page')
    vehicles = paginator.get_page(page)

    # -----------------------------
    # GRAND TOTAL
    # -----------------------------
    grand_total = parking_total + tyre_total + battery_total

    context = {
        'vehicles': vehicles,
        'parking_total': parking_total,
        'tyre_total': tyre_total,
        'battery_total': battery_total,
        'grand_total': grand_total,
        'selected_date': selected_date,
        'tyre_change': tyre_change,
        'battery_change': battery_change,
    }
    return render(request, 'report/admin_reports.html', context)