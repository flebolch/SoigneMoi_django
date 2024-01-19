from django.urls import path
from . import views


urlpatterns = [
    path('nouveau_patient/', views.register, name='nouveau_patient'),
    path('connection/', views.login, name='connection'),
    path('deconnection/', views.logout, name='deconnection'),

]
