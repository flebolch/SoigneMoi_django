from django.urls import path
from . import views


urlpatterns = [
    path('nouveau_patient/', views.register, name='nouveau_patient'),
    path('connection/', views.login, name='connection'),
    path('nouveau_visiteur/', views.register_visitor, name='nouveau_visiteur'),
    path('mon_espace_visiteur/', views.visitordashboard, name='mon_espace_visiteur'),
    path('deconnection/', views.logout, name='logout'),
]
