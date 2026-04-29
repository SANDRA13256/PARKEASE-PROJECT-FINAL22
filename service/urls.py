from django.urls import path
from . import views
app_name = 'service'
urlpatterns = [

    # SERVICE PRICES
    path('prices/', views.serviceprice_list, name='serviceprice_list'),
    path('prices/add/', views.add_serviceprice, name='add_serviceprice'),
    path('prices/update/<int:pk>/', views.update_serviceprice, name='update_serviceprice'),
    path('prices/delete/<int:pk>/', views.delete_serviceprice, name='delete_serviceprice'),

    # TYRE SERVICES
    path('tyres/', views.tyre_list, name='tyre_list'),
    path('tyres/add/', views.add_tyre, name='add_tyre'),
    path('tyres/delete/<int:pk>/', views.delete_tyre, name='delete_tyre'),
    path('tyres/receipt/<int:pk>/', views.tyre_receipt, name='tyre_receipt'),

    # BATTERY SERVICES
    path('batteries/', views.battery_list, name='battery_list'),
    path('batteries/add/', views.add_battery, name='add_battery'),
    path('batteries/delete/<int:pk>/', views.delete_battery, name='delete_battery'),
    path('batteries/receipt/<int:pk>/', views.battery_receipt, name='battery_receipt'),
    
    
]