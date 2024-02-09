from typing import Any
from django import forms
from .models import Booking, Intervention_temp, Service_temp, Doctor_temp
from datetime import datetime, timedelta


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['patient', 'service', 'intervention', 'doctor', 'date_start', 'date_stop', 'slot']
        widgets = {
            'patient': forms.HiddenInput(),
            'service': forms.HiddenInput(),
            'intervention': forms.HiddenInput(),
            'doctor': forms.HiddenInput(),
            'date_start': forms.HiddenInput(),
            'date_stop': forms.HiddenInput(),
            'slot': forms.HiddenInput(),
        }

    def clean_intevention(self):
        service = self.cleaned_data.get('service')
        intervention = self.instance

        if service and intervention:
            if not Service.objects.filter(interventions=intervention, id=service.id).exists():
                raise forms.ValidationError("This intervention does not belong to the selected service.")

        return service
