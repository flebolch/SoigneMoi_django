from django.urls import path
from . import views

urlpatterns = [
    path('gestion-des-planning/', views.planningdashboard, name='plannigdashboard'),
    path('gestion-des-medecins/', views.doctorProfileAdmin, name='doctorProfileAdmin')
    ]