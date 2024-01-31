from django.urls import path
from . import views

urlpatterns = [
    path('prendre-rendez-vous/<int:patient_id>/', views.booking, name='prendre-rendez-vous'),
    path('get-interventions/<int:service>/', views.GetInterventions.as_view(), name='interventions'),
    path('get-doctors/<int:service>/', views.GetDoctors.as_view(), name='doctors'),
]