from django.urls import path
from . import views


urlpatterns = [
    path('nouveau_patient/', views.register, name='nouveau_patient'),
    path('connection/', views.login, name='connection'),
    path('patient_info/', views.edit_profile, name='patient_info'),
    path('mon_espace_visiteur/', views.visitordashboard, name='mon_espace_visiteur'),
    path('deconnection/', views.logout, name='deconnection'),
]
