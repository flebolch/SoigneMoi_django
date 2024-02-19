from django.urls import path
from . import views

urlpatterns = [
    path('<slug:Service_slug>/', views.service, name='services_detail'),
]