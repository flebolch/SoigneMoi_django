from django.urls import path
from . import views

urlpatterns = [
    path('mes-rendez-vous/<int:patient_id>/', views.patient_appointments, name='mes-rendez-vous'),
]