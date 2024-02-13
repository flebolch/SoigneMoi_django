from django.urls import path, include
from . import views

urlpatterns = [
    path('prendre-rendez-vous/', views.booking, name='prendre-rendez-vous'),
    path('mon-rendez-vous', views.mybooking, name='mybooking'),

    path('get-interventions/<int:service>/', views.getInterventions.as_view(), name='interventions'),
    path('get-doctors/<int:service>/', views.getDoctors.as_view(), name='doctors'),
    # tmp path
    path('date/', views.date, name='date'),
    path('check-dates/<str:date_start>/<str:date_stop>/<int:service>/<int:intervention>/<int:doctor>', views.checkDates.as_view(), name='check-dates'),
    # path('check-dates/<date_start>/<date_stop>/<service>/<intervention>/<doctor>/', views.checkDates.as_view(), name='check-dates')
    #
    # path('check-date_start/<str:date>/', views.GetDate_Start.as_view(), name='date_start'),
    # path('check-date_stop/<str:date>/', views.GetDate_Stop.as_view(), name='date_stop'),
    
    path('check-slot/<int:doctor_id>/<date_start>/<date_stop>', views.GetSlot, name='getslot'),
    path('mon-rendez-vous/<int:doctor_id>/<date_start>/<date_stop>', views.GetSlot, name='getslot'),
    path('get-more-slot/<int:doctor_id>&<date_start>&<int:duration>', views.GetMoreSlot, name='getmoreslot'),
]