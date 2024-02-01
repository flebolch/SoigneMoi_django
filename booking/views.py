from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from .models import *
from django.views import View
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta

# Create your views here.
def booking(request, patient_id):
    patient  = get_object_or_404(PatientProfile_temp, pk=patient_id)
    services = Service_temp.objects.all()

    context = {
        'patient': patient,
        'services': services,
    }
    return render(request, 'booking/booking.html', context)

# ---------------------------------------------------

def GetSlot(request, doctor_id, date_start, date_stop):
    doctor = DoctorProfile_temp.objects.get(id=doctor_id)
    date_start = datetime.strptime(date_start, "%Y-%m-%d").date()
    date_stop = datetime.strptime(date_stop, "%Y-%m-%d").date()

    # Calculate the number of days required
    duration_days = (date_stop - date_start).days + 1

    # Get the number of available slots after date_start
    available_slots = TimeSlot.objects.filter(doctor_id=doctor_id, is_available=True, slot_start__date__gt=date_start)
    available_slots_count = TimeSlot.objects.filter(doctor_id=doctor_id, is_available=True, slot_start__date__gt=date_start).count()

    # Create a list of all dates from date_start to date_stop
    date_range = [date_start + timedelta(days=i) for i in range((date_stop - date_start).days + 1)]

    # Check if there is a TimeSlot for each date
    timeslots_start = []
    for date in date_range:
        timeslot = TimeSlot.objects.filter(doctor_id=doctor_id, is_available=True, slot_start__date=date)
        if timeslot.exists():
            timeslots_start.append(timeslot.first())

    error_message = ""
    if len(timeslots_start) < len(date_range):
        error_message = "Not enough available dates for the required number of days."

    # Create a range of all timeslots or placeholders from date_start to date_stop
    appointment_requested = []
    appointment_requested_available = False
    current_date = date_start
    error_message_first_choice = ""
    success_message_first_choice = ""
    while current_date <= date_stop:
        print(current_date)
        timeslot = TimeSlot.objects.filter(doctor_id=doctor_id, is_available=True, slot_start__date=current_date)
        if timeslot.exists():
            appointment_requested.append(timeslot.first())
            print(appointment_requested)
        else:
            print("enter in breack")
            break
        current_date += timedelta(days=1)

    if len(appointment_requested) < duration_days:
        appointment_requested = []
        error_message_first_choice = "Il n'y a pas de créneaux disponnibles à cette date pour le moment."
        print(error_message_first_choice)
    else :
        print('appointment_requested :', appointment_requested)
        success_message_first_choice = "dates are available"
        appointment_requested_available = True
        print('appointment_requested_available :', appointment_requested_available)

    appointment_second_choice = []
    error_message_second_choice = ""

    context = {
        'doctor': doctor,
        'date_start': date_start,
        'date_stop': date_stop,
        'duration_days': duration_days,
        'timeslots_start': timeslots_start,
        'error_message': error_message,
        'success_message_first_choice': success_message_first_choice,
        'available_slots': available_slots,
        'available_slots_count': available_slots_count,
        'error_message_first_choice': error_message_first_choice,
        'appointment_requested': appointment_requested,
        'appointment_second_choice': appointment_second_choice,
        'error_message_second_choice': error_message_second_choice,
        'appointment_requested_available': appointment_requested_available,

    }

    return render(request, 'booking/timeslot.html', context)

# def GetSlot(request, doctor_id, date_start, date_stop):
#     doctor = DoctorProfile_temp.objects.get(id=doctor_id)
#     timeslots = TimeSlot.objects.filter(doctor_id=doctor_id, is_available=True)
#     date_start = datetime.strptime(date_start, "%Y-%m-%d").date()
#     date_stop = datetime.strptime(date_stop, "%Y-%m-%d").date()

#     duration_days = 0
#     if date_start < date_stop:
#         duration = date_stop - date_start
#         duration_days = duration.days
#     elif date_start == date_stop:
#         duration_days = 1
#     else:
#         print("error date_start must be before date_stop")
#     print('duration days :', duration_days)
#     timeslots_start = TimeSlot.objects.filter(doctor_id=doctor_id, is_available=True, slot_start__date__gte=date_start)
#     print('timeslots_start :', timeslots_start)

#     appointment_range=[]
#     for days in range(duration_days):
#         appointment_range = TimeSlot.objects.filter(doctor_id=doctor_id, is_available=True, slot_start__date__gte=date_start, slot_start__date__lte=date_stop)
#         if appointment_range.exists():
#             appointment_range.append(timeslots.first())
    
#         print('appointment_range :', appointment_range)

#     context = {
#         'doctor': doctor,
#         'timeslots': timeslots,
#         'date_start': date_start,
#         'date_stop': date_stop,
#         'timeslots_start': timeslots_start,
#     }

#     return render(request, 'booking/timeslot.html', context)

class GetInterventions(View):
    def get(self, request, service, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            service = Service_temp.objects.get(id=service)
            interventions = Intervention_temp.objects.filter(service=service).order_by('name')
            data_service = {'interventions': list(interventions.values('id', 'name', 'duration'))}
            print(data_service)
            return JsonResponse(data_service)
        return HttpResponse("This is not an ajax request")
    
class GetDoctors(View):
    def get(self, request, service, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            service = Service_temp.objects.get(id=service)
            doctors = DoctorProfile_temp.objects.filter(service=service).order_by('doctorFullName')
            data_doctors = {'doctors': list(doctors.values('id', 'doctorFullName', 'speciality'))}
            print(data_doctors)
            return JsonResponse(data_doctors)
        return HttpResponse("This is not an ajax request")
    
class GetDate_Start(View):
    def get(self, request, date):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            date = datetime.strptime(date, "%Y-%m-%d").date()
            if date <= (timezone.now().date() + timedelta(days=1)):
                messages.error(request, "La date de début doit être supérieure à la date actuelle")
                return JsonResponse({"error": "La date de début doit être supérieure à la date actuelle"}, status=400)
            else:
                return JsonResponse({"success": "Date is valid"}, status=200)
        return HttpResponse("This is not an ajax request")
    

# def GetSlot(request, doctor_id, date_start, date_stop):
#     if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#         date_start = datetime.strptime(date_start, "%Y-%m-%d %H:%M:%S")
#         date_stop = datetime.strptime(date_stop, "%Y-%m-%d %H:%M:%S")
#         if date_start < timezone.now():
#             messages.error(request, "La date de début doit être supérieure à la date actuelle")
#             return JsonResponse({"error": "La date de début doit être supérieure à la date actuelle"}, status=400)
#         elif date_start >= date_stop:
#             messages.error(request, "La date de début doit être inférieure à la date de fin")
#             return JsonResponse({"error": "La date de début doit être inférieure à la date de fin"}, status=400)
#         else:
#             appointments = Appointment_temp.objects.filter(doctor=doctor_id, date_start__date=date_start.date()).order_by('date_start')
#             print(appointments)
#             data = []
#             for appointment in appointments:
#                 data.append({
#                     'date_start': appointment.date_start.strftime("%Y-%m-%d %H:%M:%S"),
#                     'date_stop': appointment.date_stop.strftime("%Y-%m-%d %H:%M:%S"),
#                 })
#             return JsonResponse(data, safe=False)
#     return HttpResponse("This is not an ajax request")