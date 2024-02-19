from django.urls import path
from . import views
from .views import getDoctorProfile,monthCalendar

urlpatterns = [
    path('nouveau-docteur/', views.newDoctor, name='newDoctor'),
    path('liste-des-docteurs/', views.listDoctors, name='listDoctors'),
    path('gestion-des-planning/', views.planningdashboard, name='planningdashboard'),
    #Data from Ajax request
    path('get-doctorsProfile/<int:doctor>/', getDoctorProfile.as_view(), name='doctorProfile'),  # Use the imported view
    path('selectedMonth/<str:date>/', monthCalendar.as_view(), name='month')
]
