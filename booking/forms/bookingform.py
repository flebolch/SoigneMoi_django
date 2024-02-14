from django import forms
from django.core.exceptions import ValidationError
from ..models import Appointment_temp
from django.utils import timezone
from datetime import datetime, timedelta


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment_temp
        fields = ['patient', 'doctor', 'intervention', 'date_start', 'date_stop']
        required_fields = ['patient', 'doctor', 'intervention']

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['date_start'].initial = self.get_default_start_time()
    #     self.fields['date_stop'].initial = self.get_default_end_time()

    def clean(self):
        cleaned_data = super().clean()
        date_start = cleaned_data.get('date_start')
        date_stop = cleaned_data.get('date_stop')

        if date_start and date_stop:  # Check that both dates are not None
            if date_stop <= date_start:
                raise ValidationError("End date must be after start date")

    # def get_default_start_time(self):
    #     return timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    # def get_default_end_time(self):
    #     return timezone.now().replace(hour=23, minute=59, second=59, microsecond=0)
        

    # class Meta:
    #     model = Appointment_temp
    #     fields = ['patient', 'doctor', 'intervention', 'date_start', 'date_stop']
    #     required_fields = ['patient', 'doctor', 'intervention']

    # def clean(self):
    #     cleaned_data = super().clean()
    #     date_start = cleaned_data.get('date_start')
    #     date_stop = cleaned_data.get('date_stop')

    #     if date_start and date_stop and date_start >= date_stop:
    #         raise ValidationError("Start date must be before end date.")

    #     # Add more validation rules as needed

    #     return cleaned_data
    
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['date_start'].initial = get_default_start_time()
    #     self.fields['date_stop'].initial = get_default_end_time()
