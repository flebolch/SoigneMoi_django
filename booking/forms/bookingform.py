from django import forms
from ..models import Appointment_temp, TimeSlot
from django.utils import timezone

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment_temp, TimeSlot
        fields = ['patient', 'doctor', 'service', 'intervention', 'date', 'time_slot', 'is_confirmed']
        widgets = {
            'patient': forms.HiddenInput(),
            'doctor': forms.HiddenInput(),
            'service': forms.HiddenInput(),
            'intervention': forms.HiddenInput(),
            'date': forms.HiddenInput(),
            'time_slot': forms.HiddenInput(),
            'is_confirmed': forms.HiddenInput(),
        }

    def clean_date(self):
        date = self.cleaned_data['date']
        if date < timezone.now().date():
            raise forms.ValidationError("The date cannot be in the past!")
        return date