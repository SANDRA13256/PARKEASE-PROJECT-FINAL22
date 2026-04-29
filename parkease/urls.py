"""
URL configuration for parkease project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from accounts import views as account_views

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    # HOME (DEFAULT PAGE)
    path('', account_views.login_staff, name='home'),
    # ACCOUNTS (LOGIN, REGISTER, DASHBOARD)
    path('accounts/', include('accounts.urls')),
    # PARKING (VEHICLES)
    path('parking/', include('parking.urls')),
    # SERVICES (TYRES, BATTERIES, PRICES)
    path('service/', include('service.urls')),
    
]