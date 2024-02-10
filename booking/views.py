from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
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


class getInterventions(View):
    def get(self, request, service, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            service = Service_temp.objects.get(id=service)
            interventions = Intervention_temp.objects.filter(service=service).order_by('name')
            data_service = {'interventions': list(interventions.values('id', 'name', 'duration'))}
            print(data_service)
            return JsonResponse(data_service)
        return HttpResponse("This is not an ajax request")
    
class getDoctors(View):
    def get(self, request, service, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            service = Service_temp.objects.get(id=service)
            doctors = DoctorProfile_temp.objects.filter(service=service).order_by('doctorFullName')
            data_doctors = {'doctors': list(doctors.values('id', 'doctorFullName', 'speciality'))}
            print(data_doctors)
            return JsonResponse(data_doctors)
        return HttpResponse("This is not an ajax request")
    
def date(request):
    return render(request, 'booking/check-date.html')
    
class checkDates(View):
    def get(self, request, date_start, date_stop):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Only for testing purpose, in production, the patient_id will be passed as a parameter

            
            date_start = datetime.strptime(date_start, "%Y-%m-%d").date()
            date_stop = datetime.strptime(date_stop, "%Y-%m-%d").date()
            patient_id = 1

            result = isPatientAvailable(patient_id, date_start, date_stop)
            print('result:',result)
            
            
            # chekink if date is greater than today
            if date_start < timezone.now().date():
                return JsonResponse({"errorDateStart": "Merci de choisir une date future."}, status=400)
            elif date_start > date_stop:
                return JsonResponse({"errorDateStop": "La date de début ne peut pas être après la date de fin."}, status=400)
            elif isPatientAvailable(patient_id, date_start, date_stop) == False:
                return JsonResponse({"errorDateStart": "Vous avez déjà un rendez-vous prévu sur cette plage de rendez-vous."}, status=400)
            else: 
                return JsonResponse({"success": "Date is valid"}, status=200)
        return HttpResponse("This is not an ajax request")

def isPatientAvailable(patient_id, date_start, date_stop):
    patient = get_object_or_404(PatientProfile_temp, pk=patient_id)
    all_appointments = Appointment_temp.objects.filter(patient=patient_id)
    patient_available = False

    # Convert date_start and date_stop to datetime objects
    date_start = timezone.make_aware(datetime.combine(date_start, time.min))
    date_stop = timezone.make_aware(datetime.combine(date_stop, time.max))

    for appointment in all_appointments:
        appointment_start_date = appointment.date_start.date()
        appointment_stop_date = appointment.date_stop.date()
        if date_start >= appointment.date_start and date_start <= appointment.date_stop:
            patient_available = False
        elif date_stop >= appointment.date_start and date_stop <= appointment.date_stop:
            patient_available = False
        else:
            patient_available = True
    return patient_available
    


# class GetDate_Start(View):
#     def get(self, request, date):
#         if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#             date = datetime.strptime(date, "%Y-%m-%d").date()
#             date_minimum = timezone.now().date() + timedelta(days=1)
#             if date <= date_minimum:
#                 date_mimum_format = date_minimum.strftime("%d-%m-%Y")
#                 return JsonResponse({"error": f"Merci de choisir une date après le {date_mimum_format}"}, status=400)
#             else:
#                 return JsonResponse({"success": "Date is valid"}, status=200)
#         return HttpResponse("This is not an ajax request")
    
# class GetDate_Stop(View):
#     def get(self, request, date):
#         if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#             date = datetime.strptime(date, "%Y-%m-%d").date()
#             date_minimum = timezone.now().date() + timedelta(days=1)
#             if date <= date_minimum:
#                 date_mimum_format = date_minimum.strftime("%d-%m-%Y")
#                 return JsonResponse({"error": f"Merci de choisir une date après le {date_mimum_format}"}, status=400)
#             else:
#                 return JsonResponse({"success": "Date is valid"}, status=200)
#         return HttpResponse("This is not an ajax request")
    

# class checkDate(View):
#     def get(self, request, date_start, date_stop):
#         if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#             date_start = datetime.strptime(date_start, "%Y-%m-%d").date()
#             date_stop = datetime.strptime(date_stop, "%Y-%m-%d").date()
#             if date_start > date_stop:
#                 return JsonResponse({"error": "La date de début ne peut pas être après la date de fin."}, status=400)
#             else:
#                 return JsonResponse({"success": "Date is valid"}, status=200)
#         return HttpResponse("This is not an ajax request")
    

# Getslot Raw method

# def GetSlot(request, doctor_id, date_start, date_stop):
#     try:
#         doctor = DoctorProfile_temp.objects.get(id=doctor_id)
#         date_start = datetime.strptime(date_start, "%Y-%m-%d").date()
#         date_stop = datetime.strptime(date_stop, "%Y-%m-%d").date()

#         if date_start > date_stop:
#             return HttpResponseBadRequest("Invalid date range: date_start cannot be after date_stop")

#     except DoctorProfile_temp.DoesNotExist:
#         return HttpResponseBadRequest("Invalid doctor_id")

#     except ValueError:
#         return HttpResponseBadRequest("Invalid date format")

#     # Calculate the number of days required
#     duration_days = (date_stop - date_start).days + 1

#     # Get the number of available slots after date_start
#     available_slots = TimeSlot.objects.filter(doctor_id=doctor_id, is_available=True, slot_start__date__gt=date_start)
#     available_slots_count = TimeSlot.objects.filter(doctor_id=doctor_id, is_available=True, slot_start__date__gt=date_start).count()

#     # Create a list of all dates from date_start to date_stop
#     date_range = [date_start + timedelta(days=i) for i in range((date_stop - date_start).days + 1)]

#     # Check if there is a TimeSlot for each date
#     timeslots_start = []
#     for date in date_range:
#         timeslot = TimeSlot.objects.filter(doctor_id=doctor_id, is_available=True, slot_start__date=date)
#         if timeslot.exists():
#             timeslots_start.append(timeslot.first())

#     error_message = ""
#     if len(timeslots_start) < len(date_range):
#         error_message = "Not enough available dates for the required number of days."
    
#         # Create a range of all timeslots or placeholders from date_start to date_stop
#     appointment_requested = []
#     appointment_requested_available = False
#     current_date = date_start
#     error_message_first_choice = ""
#     success_message_first_choice = ""
#     while current_date <= date_stop:
#         timeslot = TimeSlot.objects.filter(doctor_id=doctor_id, is_available=True, slot_start__date=current_date)
#         if timeslot.exists():
#             appointment_requested.append(timeslot.first())
#         else:
#             break
#         current_date += timedelta(days=1)

       
#     if len(appointment_requested) == duration_days:
#         success_message_first_choice = "dates are available"
#         appointment_requested_available = True
#     else:
#         appointment_requested = []
#         error_message_first_choice = "Il n'y a pas de créneaux disponnibles à cette date pour le moment."

#     context = {
#         'doctor': doctor,
#         'date_start': date_start,
#         'date_stop': date_stop,
#         'duration_days': duration_days,
#         'timeslots_start': timeslots_start,
#         'error_message': error_message,
#         'success_message_first_choice': success_message_first_choice,
#         'available_slots': available_slots,
#         'available_slots_count': available_slots_count,
#         'error_message_first_choice': error_message_first_choice,
#         'appointment_requested': appointment_requested,
#         'appointment_requested_available': appointment_requested_available,
#     }

#     return render(request, 'booking/timeslot.html', context)

# end GetSlot raw method
    
def GetSlot(request):
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor_id')
        date_start = request.POST.get('date_start')
        date_stop = request.POST.get('date_stop')
        try:
            doctor = DoctorProfile_temp.objects.get(id=doctor_id)
            date_start = datetime.strptime(date_start, "%Y-%m-%d").date()
            date_stop = datetime.strptime(date_stop, "%Y-%m-%d").date()

            if date_start > date_stop:
                return HttpResponseBadRequest("Invalid date range: date_start cannot be after date_stop")

        except DoctorProfile_temp.DoesNotExist:
            return HttpResponseBadRequest("Invalid doctor_id")

        except ValueError:
            return HttpResponseBadRequest("Invalid date format")

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
            timeslot = TimeSlot.objects.filter(doctor_id=doctor_id, is_available=True, slot_start__date=current_date)
            if timeslot.exists():
                appointment_requested.append(timeslot.first())
            else:
                break
            current_date += timedelta(days=1)

        
        if len(appointment_requested) == duration_days:
            success_message_first_choice = "dates are available"
            appointment_requested_available = True
        else:
            appointment_requested = []
            error_message_first_choice = "Il n'y a pas de créneaux disponnibles à cette date pour le moment."

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
            'appointment_requested_available': appointment_requested_available,
        }

        return render(request, 'booking/timeslot.html', context)


# ---------test get more slot----------------

def GetMoreSlot(request, doctor_id, date_start, duration):
    doctor = DoctorProfile_temp.objects.get(id=doctor_id)
    date_start = datetime.strptime(date_start, "%Y-%m-%d").date()


    # Nulmber of days required
    duration_days = duration
    appointment_seconde_choice_available = False
    success_message_second_choice = ""
    error_message_second_choice = ""
    # Get the number of available slots after date_start
    available_slots = TimeSlot.objects.filter(doctor_id=doctor_id, is_available=True, slot_start__date__gt=date_start).order_by('slot_start')
    print(available_slots)
    available_slots_count = TimeSlot.objects.filter(doctor_id=doctor_id, is_available=True, slot_start__date__gt=date_start).count()

    appointment_second_choice = find_consecutive_slots(available_slots, duration_days)
    print(appointment_second_choice)
    if appointment_second_choice is not None:
        success_message_second_choice = "dates are available"
        appointment_seconde_choice_available = True
    else:
        error_message_second_choice = "Il n'y a pas de créneaux disponnibles à cette date pour le moment."

    context = {
        'doctor': doctor,
        'date_start': date_start,
        'duration_days': duration_days,
        'available_slots_count': available_slots_count,
        'available_slots': available_slots,
        'appointment_second_choice': appointment_second_choice,
        'success_message_second_choice': success_message_second_choice,
        'appointment_seconde_choice_available': appointment_seconde_choice_available,
        'error_message_second_choice': error_message_second_choice,

    }
    return render(request, 'booking/moreslot.html', context)

def find_consecutive_slots(available_slots, duration_days):
    
    
    for i in range(len(available_slots) - duration_days + 1):
        # Get a range of slots of length 'duration_days'
        slot_range = available_slots[i:i+duration_days]
        print(slot_range)
       
       # Check if the slots in the range are consecutive
        is_consecutive = True
        for j in range(duration_days - 1):
            print(slot_range[j+1].slot_start - slot_range[j].slot_start)
            if (slot_range[j+1].slot_start - slot_range[j].slot_start).days != 1:
                is_consecutive = False
                break

        if is_consecutive:
            print('len of slots :',len(slot_range))
            return slot_range

    return None

# def register_appointment(request, patient_id, doctor_id, intervention, date_start, date_stop):
#     if request.method == 'POST':
