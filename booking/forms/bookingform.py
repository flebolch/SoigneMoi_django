from django import forms
from ..models import Appointment_temp
from django.utils import timezone

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment_temp
        fields = ['patient', 'doctor', 'intervention', 'date_start', 'date_stop']