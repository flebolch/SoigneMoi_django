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
    for service in services:
        print(service.id)

    context = {
        'patient': patient,
        'services': services,
    }
    return render(request, 'booking/booking.html', context)


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
    