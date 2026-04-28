from django.urls import path
from . import views
app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_staff, name='register'),
    path('login/', views.login_staff, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_staff, name='logout'),
    # Dashboards
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manager-dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('attendant-dashboard/', views.attendant_dashboard, name='attendant_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
