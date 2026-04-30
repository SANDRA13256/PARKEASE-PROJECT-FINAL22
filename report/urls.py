from django.urls import path
from . import views
app_name = 'report'
urlpatterns = [
path('admin/reports/', views.admin_reports, name='admin_reports'),


]
