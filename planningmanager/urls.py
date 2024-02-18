from django.urls import path
from . import views

urlpatterns = [
    path('nouveau-docteur/', views.newDoctor, name='newDoctor'),
    path('liste-des-docteurs/', views.listDoctors, name='listDoctors'),
    path('gestion-des-planning/', views.planningdashboard, name='planningdashboard'),
    #Data from Ajax request
    path('get-doctorsProfile/<int:doctor>/', views.getDoctorProfile.as_view(), name='doctorProfile'),
    ]