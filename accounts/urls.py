from django.urls import path
from . import views
app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_staff, name='register'),
    path('login/', views.login_staff, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_staff, name='logout'),
    path('users/', views.user_list, name='user_list'),

    path('users/add/', views.add_user, name='add_user'),
    path('users/update/<int:pk>/', views.update_user, name='update_user'),
    path('users/delete/<int:pk>/', views.delete_user, name='delete_user'),
     # Dashboards
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manager-dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('attendant-dashboard/', views.attendant_dashboard, name='attendant_dashboard'),
    
    
]
