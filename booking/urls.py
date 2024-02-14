from django.urls import path, include
from . import views

urlpatterns = [
    #form page
    path('prendre-rendez-vous/', views.booking, name='prendre-rendez-vous'),
    #populate fields request
    path('get-interventions/<int:service>/', views.getInterventions.as_view(), name='interventions'),
    path('get-doctors/<int:service>/', views.getDoctors.as_view(), name='doctors'),
    #check request
    path('create-appointment/<int:service>/<int:intervention>/<int:doctor>/<str:dateStart>/<str:dateStop>/', views.CreateAppointment.as_view(), name='create_appointment'),
    ]