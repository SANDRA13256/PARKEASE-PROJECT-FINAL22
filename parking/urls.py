from django.urls import path
from . import views
app_name = 'parking'
urlpatterns = [
    # Vehicle Categories
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.add_category, name='add_category'),
    path('service-prices/', views.serviceprice_list, name='serviceprice_list'),
    
    
    # Vehicle Registration
    path('', views.vehicle_list, name='vehicle_list'),
    path('register/', views.register_vehicle, name='register_vehicle'),
    path('update/<int:pk>/', views.update_vehicle, name='update_vehicle'),
    path('delete/<int:pk>/', views.delete_vehicle, name='delete_vehicle'),
    path('signout/<int:pk>/', views.signout_vehicle, name='signout_vehicle'),
    
]
