from django.urls import path
from . import views

urlpatterns = [
    # path('gestion-des-planning/', views.planningdashboard, name='plannigdashboard'),
    path('nouveau-docteur/', views.newDoctor, name='newDoctor'),
    path('liste-des-docteurs/', views.listDoctors, name='listDoctors'),
    ]