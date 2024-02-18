from django.urls import path, reverse
from . import views

urlpatterns = [
    path('nouveau-docteur/', views.newDoctor, name='newDoctor'),
    path('liste-des-docteurs/', views.listDoctors, name='listDoctors'),
    path('gestion-des-planning/', views.planningdashboard, name='planningdashboard'),
    ]