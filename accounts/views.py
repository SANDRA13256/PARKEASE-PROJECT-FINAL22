from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import StaffForm, StaffLoginForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum
from parking.models import VehicleRegistration
from service.models import TyreService, BatteryService
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .forms import StaffForm   

from django.contrib.auth import get_user_model
User = get_user_model()
# Registering staff
def register_staff(request):
    form = StaffForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            messages.success(request, "Staff account created successfully")
            return redirect('login')

    return render(request, 'register.html', {'form': form})



# Logging in staff

def login_staff(request):
    form = StaffLoginForm(request, data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('accounts:dashboard')
        else:
            print(form.errors)  

    return render(request, 'login.html', {'form': form})


# Dashboard

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    user = request.user

    if user.role == 'ADMIN':
        return render(request, 'dashboards/admin_dashboard.html')

    elif user.role == 'MANAGER':
        return render(request, 'dashboards/manager_dashboard.html')

    elif user.role == 'ATTENDANT':
        return render(request, 'dashboards/attendant_dashboard.html')

    return redirect('accounts:login')


# Logout

def logout_staff(request):
    logout(request)
    return redirect('accounts:login')

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    user = request.user

    if user.role == 'ADMIN':
        return render(request, 'dashboards/admin_dashboard.html')

    elif user.role == 'MANAGER':
        return render(request, 'dashboards/manager_dashboard.html')

    elif user.role == 'ATTENDANT':
        return render(request, 'dashboards/attendant_dashboard.html')

    return redirect('accounts:login')


@login_required
def admin_dashboard(request):
    if request.user.role != 'ADMIN':
        return redirect('accounts:login')
    return render(request, 'dashboards/admin_dashboard.html')

def admin_dashboard(request):
    
    selected_date = request.GET.get('date')

    if selected_date:
        selected_date = timezone.datetime.strptime(selected_date, "%Y-%m-%d").date()
    else:
        selected_date = timezone.now().date()

    
    # this is for Parking (only signed out)
    parking_today = VehicleRegistration.objects.filter(
        status='signed_out',
        departure_time__date=selected_date
    )

    parking_total = 0

    for v in parking_today:
        if v.rate == 'day':
            parking_total += v.type.day_rate
        elif v.rate == 'night':
            parking_total += v.type.night_rate
        elif v.rate == 'short':
            parking_total += v.type.short

    # Tyre section

    tyre_today = TyreService.objects.filter(date__date=selected_date)
    tyre_total = tyre_today.aggregate(total=Sum('price'))['total'] or 0


    # Battery section

    battery_today = BatteryService.objects.filter(date__date=selected_date)
    battery_total = battery_today.aggregate(total=Sum('price'))['total'] or 0

    # Total
    total_revenue = parking_total + tyre_total + battery_total

    context = {
        'selected_date': selected_date,
        'parking_total': parking_total,
        'tyre_total': tyre_total,
        'battery_total': battery_total,
        'total_revenue': total_revenue,

        'parking_records': parking_today,
        'tyre_records': tyre_today,
        'battery_records': battery_today,
    }

    return render(request, 'admin_dashboard.html', context)


@login_required
def manager_dashboard(request):
    if request.user.role != 'MANAGER':
        return redirect('accounts:login')

    today = timezone.now().date()

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    tyres = TyreService.objects.all()
    batteries = BatteryService.objects.all()

    #  this is where Filtering is done
    if start_date and end_date:
        tyres = tyres.filter(date__date__range=[start_date, end_date])
        batteries = batteries.filter(date__date__range=[start_date, end_date])
    else:
        tyres = tyres.filter(date__date=today)
        batteries = batteries.filter(date__date=today)

    # Totals
    tyre_total = tyres.aggregate(total=Sum('price'))['total'] or 0
    battery_total = batteries.aggregate(total=Sum('price'))['total'] or 0

    context = {
        'tyres': tyres.order_by('-date'),
        'batteries': batteries.order_by('-date'),
        'tyre_total': tyre_total,
        'battery_total': battery_total,
        'total_revenue': tyre_total + battery_total,
        'tyre_count': tyres.count(),
        'battery_count': batteries.count(),
    }

    return render(request, 'dashboards/manager_dashboard.html', context)


@login_required
def attendant_dashboard(request):
    if request.user.role != 'ATTENDANT':
        return redirect('accounts:login')
    return render(request, 'dashboards/attendant_dashboard.html')

User = get_user_model()


@login_required
def user_list(request):
    if request.user.role != 'ADMIN':
        return redirect('accounts:login')

    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})


@login_required
def delete_user(request, pk):
    if request.user.role != 'ADMIN':
        return redirect('accounts:login')

    user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        user.delete()
        return redirect('accounts:user_list')

    return render(request, 'confirm_delete.html', {'object': user})


@login_required
def user_list(request):
    if not request.user.is_superuser:
        return redirect('accounts:login')

    users = User.objects.all()
    return render(request, 'accounts/user_list.html', {'users': users})

@login_required
def add_user(request):
    if request.user.role != 'ADMIN':
        return redirect('accounts:login')

    form = StaffForm(request.POST or None)

    if form.is_valid():
        user = form.save(commit=False)

        # the hashed password is here
        user.set_password(form.cleaned_data['password'])

        user.save()
        return redirect('accounts:user_list')

    return render(request, 'accounts/user_form.html', {'form': form})

@login_required
def update_user(request, pk):
    if not request.user.is_superuser:
        return redirect('accounts:login')

    user = get_object_or_404(User, pk=pk)
    form = StaffForm(request.POST or None, instance=user)

    if form.is_valid():
        form.save()
        return redirect('accounts:user_list')

    return render(request, 'accounts/user_form.html', {'form': form})


@login_required
def delete_user(request, pk):
    if not request.user.is_superuser:
        return redirect('accounts:login')

    user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        user.delete()
        return redirect('accounts:user_list')

    return render(request, 'confirm_delete.html', {'object': user})

@login_required
def user_list(request):
    users = User.objects.all()
    return render(request, 'accounts/user_list.html', {'users': users})


@login_required
def add_user(request):
    form = StaffForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('accounts:user_list')

    return render(request, 'accounts/user_form.html', {'form': form})


@login_required
def update_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    form = StaffForm(request.POST or None, instance=user)

    if form.is_valid():
        form.save()
        return redirect('accounts:user_list')

    return render(request, 'accounts/user_form.html', {'form': form})


@login_required
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)

    if request.method == "POST":
        user.delete()
        return redirect('accounts:user_list')

    return render(request, 'accounts/confirm_delete.html', {'object': user})





    
    