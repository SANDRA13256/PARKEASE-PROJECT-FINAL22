from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import StaffForm, StaffLoginForm
from django.contrib.auth.decorators import login_required



# REGISTER STAFF

def register_staff(request):
    form = StaffForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            messages.success(request, "Staff account created successfully")
            return redirect('login')

    return render(request, 'register.html', {'form': form})



# LOGIN STAFF

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


# DASHBOARD

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


# LOGOUT

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


@login_required
def manager_dashboard(request):
    if request.user.role != 'MANAGER':
        return redirect('accounts:login')
    return render(request, 'dashboards/manager_dashboard.html')


@login_required
def attendant_dashboard(request):
    if request.user.role != 'ATTENDANT':
        return redirect('accounts:login')
    return render(request, 'dashboards/attendant_dashboard.html')





    
    