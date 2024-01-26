from django.shortcuts import render, get_object_or_404
from .models import Appointment, PatientProfile_temp
from django.utils import timezone

def patient_appointments(request, patient_id):
    patient = get_object_or_404(PatientProfile_temp, pk=patient_id)
    all_appointments = Appointment.objects.filter(patient=patient)

    past_appointments = all_appointments.filter(date_stop__lt=timezone.now())
    future_appointments = all_appointments.filter(date_start__gt=timezone.now())
    current_appointments = all_appointments.filter(date_start__lte=timezone.now(), date_stop__gte=timezone.now())
    print('all:', all_appointments)
    print('past:', past_appointments)
    print('future:', future_appointments)
    print('current:', current_appointments)

    context = {
        'patient': patient,
        'past_appointments': past_appointments,
        'future_appointments': future_appointments,
        'current_appointments': current_appointments,
        'all_appointments': all_appointments,
    }

    return render(request, 'appointment/patient_appointments.html', context)