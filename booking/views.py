from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from .models import *
from .forms.bookingform import AppointmentForm
from django.views import View
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta

# Create your views here.
def booking(request):
    # patient  = get_object_or_404(PatientProfile_temp, pk=patient_id)
    # Test value for patient_id
    patient = get_object_or_404(PatientProfile_temp, pk=1)
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
            data_service = {'interventions': list(interventions.values('id', 'name'))}
            return JsonResponse(data_service)
        return HttpResponse("This is not an ajax request")


class getDoctors(View):
    def get(self, request, service, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            service = Service_temp.objects.get(id=service)
            doctors = DoctorProfile_temp.objects.filter(service=service).order_by('doctorFullName')
            data_doctors = {'doctors': list(doctors.values('id', 'doctorFullName', 'speciality'))}
            return JsonResponse(data_doctors)
        return HttpResponse("This is not an ajax request")
    
def date(request):
    return render(request, 'booking/check-date.html')

class createAppointment(View):
    def get(self, request, service, intervention, doctor, dateStart, dateStop):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            patient = get_object_or_404(PatientProfile_temp, pk=1)
            service = Service_temp.objects.get(id=service)
            doctor = DoctorProfile_temp.objects.get(id=doctor)
            intervention = Intervention_temp.objects.get(id=intervention)
            dateStart = datetime.strptime(dateStart, "%Y-%m-%d").date()
            dateStop = datetime.strptime(dateStop, "%Y-%m-%d").date()
            duration_days = duration(request, dateStart, dateStop)
            print('CreateAppointment value:', dateStart, dateStop, service, intervention, doctor)

            if not checkStartdate(request, dateStart):
                return JsonResponse({'errorDateStart': 'Merci de choisir une date future.'}, status=400)
                print('dateStart is incorrect')

            elif not checkStopdate(request, dateStop, dateStart):
                return JsonResponse({'errorDateStop': 'La date de début ne peut pas être après la date de fin.'}, status=400)
                print('dateStop is incorrect')

            elif not isPatientAvailable(patient, dateStop, dateStart):
                return JsonResponse({"errorDateStart": "Vous avez déjà un rendez-vous prévu sur cette plage de rendez-vous."}, status=400)
            
            elif not getSlot(request, doctor, dateStart, dateStop, duration_days):
                return JsonResponse({"errorDateStart": "Il n'y a pas assez de créneaux disponibles pour la durée demandée."}, status=400)

            else:
                 print('duration:', duration_days)
                
            return JsonResponse({'message': f'Valider votre rendez-vous d\'une durée de {duration_days} jour(s) avec le docteur {doctor} :'}) 
            

        return HttpResponse("This is not an ajax request")
    

        
        
#check if date start is correct
def checkStartdate(request, dateStart):
    today = datetime.now().date()
    if dateStart >= today:
        return True
    return False
        
#check if date stop is correct
def checkStopdate(request, dateStart, dateStop):
    if dateStop <= dateStart:
        return True
    return False

#calculate duration
def duration(request, dateStart, dateStop):
    duration_days = (dateStop - dateStart).days + 1
    return duration_days
        
#check if patient is available
def isPatientAvailable(patient, dateStart, dateStop):
    print('enter isPatientAvailable')
    all_appointments = Appointment_temp.objects.filter(patient=patient)
    print('all_appointments:', all_appointments)
    patient_available = True

   # Convert date_start and date_stop to datetime objects
    date_start = timezone.make_aware(datetime.combine(dateStart, time.min))
    date_stop = timezone.make_aware(datetime.combine(dateStop, time.max))
    for appointment in all_appointments:
        if date_start <= appointment.date_stop and date_stop >= appointment.date_start:
            return False
    return True
        
#find available slots
def getSlot(request, doctor, dateStart, dateStop, duration_days):
    # Get the number of available slots after date_start
    date_start = datetime.combine(dateStart, time(10, 0, 0))
    date_stop = datetime.combine(dateStop, time(18, 0, 0))
    timeslotsToSave = []
    available_slots = TimeSlot.objects.filter(doctor=doctor, is_available=True, slot_end__gte=date_start)

    if available_slots.count() < duration_days:
        print('enter first test')
        return False
 
    date_range = []
    current_date = date_start
    while current_date <= date_stop:
        date_range.append(current_date.strftime('%Y-%m-%d'))  # Convert datetime to date string
        current_date += timedelta(days=1)

    for date in date_range:
        date = datetime.strptime(date, '%Y-%m-%d').date()
        print('date:', date)
        timeslot = TimeSlot.objects.filter(doctor=doctor, is_available=True, slot_start__date=date)
        if timeslot.exists():
            timeslotsToSave.append(timeslot.first())

    if len(timeslotsToSave) == duration_days:
        timeslotsToSave = [timeslot.id for timeslot in timeslotsToSave]
        return timeslotsToSave
    elif len(timeslotsToSave) < len(date_range):
        timeslotsToSave = []
        return timeslotsToSave


class registerAppointment(View):
    def get(self, request, intervention, doctor, dateStart, dateStop):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            #update TimeSlot
            d_Start = datetime.strptime(dateStart, "%Y-%m-%d")
            d_Stop = datetime.strptime(dateStop, "%Y-%m-%d")
            duration_days = duration(request, d_Start, d_Stop)
            timeslotsToSave = getSlot(request, doctor, d_Start, d_Stop, duration_days)
            timeslots = TimeSlot.objects.filter(id__in=timeslotsToSave)
            for timeslot in timeslots:
                timeslot.patient_available -= 1
                if timeslot.patient_available == 0:
                    timeslot.is_available = False
                timeslot.save()
            #update the appointment
            patient = get_object_or_404(PatientProfile_temp, pk=1)
            doctor = DoctorProfile_temp.objects.get(id=doctor)
            intervention = Intervention_temp.objects.get(id=intervention)
            dateStart = datetime.combine(datetime.strptime(dateStart, "%Y-%m-%d"), time.min)
            dateStop = datetime.combine(datetime.strptime(dateStop, "%Y-%m-%d"), time.max)
            Appointment = Appointment_temp(patient=patient, doctor=doctor, intervention=intervention, date_start=dateStart, date_stop=dateStop)
            print('Appointment:', Appointment)
            Appointment.save()
            form = AppointmentForm()  # Replace MyForm with the actual form class
            if form.is_valid():
                form.save()
                return JsonResponse({'message': 'Appointment created successfully'})
            else:
                return JsonResponse({'error': 'Invalid form data'}, status=400)
        else:
            return JsonResponse({'error': 'Invalid request method'}, status=405)
