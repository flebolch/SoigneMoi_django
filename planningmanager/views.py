from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .forms.newdoctor import DoctorForm, AccountForm
from .models import Account, DoctorProfile, Service
from django.views import View
from django.contrib import messages
from datetime import date
from django.db import IntegrityError, transaction
from django.core import serializers
from .models import DoctorProfile, Service, TimeSlot
import random, re
from calendar import HTMLCalendar

class monthCalendar(View):
    def get(self, request, date, doctor):
        date = date
        doctor = doctor
        year, month = date.split('-')
        doctorTimeslots = getTimeslots(request, doctor)
        year = int(year)
        month = int(month)
        monthDoctorTimeslots = filterTimeslots(request, doctorTimeslots, year, month)
        print('monthDoctorTimeslots:', monthDoctorTimeslots)
        print(year, month)
        month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        month_number = int(month) - 1
        month_name = month_names[month_number]
        calendar = HTMLCalendar()
        html_calendar = calendar.formatmonth(year, month)
        html_calendar = processCalendar(html_calendar, year, month_name)
        html_calendar = addActualTimeslots(html_calendar, monthDoctorTimeslots)
        return HttpResponse(html_calendar)
    
def addActualTimeslots(html_calendar, monthDoctorTimeslots): 
    for day in monthDoctorTimeslots:
        html_calendar = re.sub(rf'<td class="(.*?)">{day}</td>', rf'<td class="\1"><span class="dayAvailable">{day}</span></td>', html_calendar)
    return html_calendar

def getTimeslots(request, doctor):
    timelots = TimeSlot.objects.filter(doctor=doctor)
    print('timelots:', timelots)
    doctorTimeslots = []
    for timeslot in timelots:
        doctorTimeslots.append(timeslot.slot_start.strftime('%Y-%m-%d'))
    return doctorTimeslots

def filterTimeslots(request, doctorTimeslots, year, month):
    monthDoctorTimeslots = []
    for timeslot in doctorTimeslots:
        slot_year, slot_month, slot_day = timeslot.split('-')
        if int(slot_year) == year and int(slot_month) == month:
            monthDoctorTimeslots.append(slot_day)
    return monthDoctorTimeslots



def processCalendar(html_calendar, year, month_name):

    #Convert the month into French
    month_eng_to_fre = {
        'January': 'Janvier',
        'February': 'Février',
        'March': 'Mars',
        'April': 'Avril',
        'May': 'Mai',
        'June': 'Juin',
        'July': 'Juillet',
        'August': 'Août',
        'September': 'Septembre',
        'October': 'Octobre',
        'November': 'Novembre',
        'December': 'Décembre'
    }
    # Get the French month name
    fre_month_name = month_eng_to_fre[month_name]

    #Removes the year from the month name
    html_calendar = re.sub(r'(?<=<tr><th colspan="7" class="month">).+?(?=</th></tr>)', '', html_calendar)

    # Add the French month name and the year to the calendar
    # html_calendar = html_calendar.replace('<table border="0" cellpadding="0" cellspacing="0" class="month"><tr><th colspan="7" class="month"></th></tr>', f'<divclass="month"><ul><liclass="prev">&#10094;</li><liclass="next">&#10095;</li><li>{fre_month_name}<br><spanstyle="font-size:18px">{year}</span></li></ul></div>')
    # html_calendar = re.sub(r'<table border="0" cellpadding="0" cellspacing="0" class="month">\n<tr><th colspan="7" class="month"></th></tr>', '', html_calendar)
    html_calendar = re.sub(r'<table border="0" cellpadding="0" cellspacing="0" class="month">', '', html_calendar)
    # prepend = f'<div class="month"><ul><li class="prev">&#10094;</li><li class="next">&#10095;</li><li>{fre_month_name}<br><span style="font-size:18px">{year}</span></li></ul></div><ul class="weekdays"><li>Lun</li><li>Mar</li><li>Mer</li<li>jeu</li><li>Ven</li><li>Sam</li><li>Dim</li></ul><table border="0" cellpadding="0" cellspacing="0" class="month"><tr><th colspan="7" class="month"></th></tr>'
    # prepend = f'<div class="month"><ul><li class="prev">&#10094;</li><li class="next">&#10095;</li><li>{fre_month_name}<br><span style="font-size:18px">{year}</span></li></ul></div><ul class="weekdays"><table border="0" cellpadding="0" cellspacing="0" class="month"><tr><th colspan="7" class="month"></th></tr><tr class="weekdays"><th class="mon">Lun</th><th class="tue">Mar</th><th class="wed">Mer</th><th class="thu">Jeu</th><th class="fri">Ven</th><th class="sat">Sam</th><th class="sun">Dim</th></tr>'
    # prepend = f'<div class="month"><ul><li class="prev">&#10094;</li><li class="next">&#10095;</li><li>{fre_month_name}<br><span style="font-size:18px">{year}</span></li></ul></div><ul class="weekdays"><table border="0" cellpadding="0" cellspacing="0" class="month"><tr><th colspan="7" class="month"></th></tr><tr class="weekdays"><td class="mon">Lun</td><td class="tue">Mar</td><td class="wed">Mer</td><td class="thu">Jeu</td><td class="fri">Ven</td><td class="sat">Sam</td><td class="sun">Dim</td></tr>'
    prepend = f'<div class="month"><ul><li class="prev">&#10094;</li><li class="next">&#10095;</li><li>{fre_month_name}<br><span style="font-size:18px">{year}</span></li></ul></div><ul class="weekdays"><table border="0" cellpadding="0" cellspacing="0" class="month"></tr><tr class="weekdays"><td class="mon">Lun</td><td class="tue">Mar</td><td class="wed">Mer</td><td class="thu">Jeu</td><td class="fri">Ven</td><td class="sat">Sam</td><td class="sun">Dim</td></tr>'
    html_calendar = prepend + html_calendar
    html_calendar = re.sub(r'<tr><th class="mon">Mon</th><th class="tue">Tue</th><th class="wed">Wed</th><th class="thu">Thu</th><th class="fri">Fri</th><th class="sat">Sat</th><th class="sun">Sun</th></tr>', '', html_calendar)
    html_calendar = re.sub(r'<th colspan="7" class="month"></th></tr>', '', html_calendar)
    html_calendar = html_calendar.replace('<tr><td', '<tr class="days"><td')
    return html_calendar

def planningdashboard(request):
    doctors = DoctorProfile.objects.all()
    context = {
        'doctors': doctors
    }
    return render(request, 'planningmanager/planningdashboard.html', context)

class getDoctorProfile(View):
    def get(self, request, doctor, *args, **kwargs):
        doctorProfile = DoctorProfile.objects.filter(id=doctor)
        timeslots= getTimeslots(request, doctor)

        doctorProfile_info = {
            'doctorProfile': list(doctorProfile.values('speciality', 'matricule', 'service__name', 'user__username')),
            'timeslots': timeslots
        }
        return JsonResponse(doctorProfile_info)
    


def newDoctor(request):
    if request.method == 'POST':
        doctor_form = DoctorForm(request.POST)
        account_form = AccountForm(request.POST)
        try:

            if doctor_form.is_valid() and account_form.is_valid():
                with transaction.atomic():
                    account = account_form.save(commit=False)
                    doctor = doctor_form.save(commit=False)

                    # create user account
                    new_password_tmp = GeneratePassordTemp()
                    password = new_password_tmp
                    username = account_form.cleaned_data['username']
                    first_name = account_form.cleaned_data['first_name']
                    last_name = account_form.cleaned_data['last_name']
                    user = Account.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password)
                    print('line 33 views.py')
                    user.is_active = True

                    # create doctor profile
                    doctor.user = user
                    service = doctor_form.cleaned_data['service']
                    print('line 38 views.py Servive is :',service)
                    speciality = doctor_form.cleaned_data['speciality']
                    matricule = generateMatricule(first_name, last_name)
                    doctor = DoctorProfile.objects.create(user=user, service=service, speciality=speciality, matricule=matricule, password_temp=new_password_tmp)
                    print('line 42 views.py')
                    
                    # save user and doctor
                    user.save()
                    doctor.save()
                    messages.success(request, 'Le médecin a été ajouté avec succès')
                
        except IntegrityError:
            messages.error(request, 'Adresse email déjà utilisée')
            return render(request, 'planningmanager/newDoctorProfile.html', {'doctor_form': doctor_form, 'account_form': account_form})

        else:
            for field, errors in account_form.errors.items():
                for error in errors:
                    messages.error(request, error, extra_tags='danger')
            return render(request, 'planningmanager/newDoctorProfile.html', {'doctor_form': doctor_form, 'account_form': account_form})
    else:

        context = {
            'doctor_form': DoctorForm(),
            'account_form': AccountForm()
        }
    return render(request, 'planningmanager/newDoctorProfile.html', context)



def GeneratePassordTemp():
    pwdlenght = 10
    characters = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()')
    temp_password = ''.join(random.choice(characters) for i in range(pwdlenght))
    return temp_password

def generateMatricule(first_name, last_name):
    current_date = date.today()
    first_n = first_name[0]
    last_n = last_name[0]
    y = str(current_date.year)[-2:]
    m = str(current_date.month).zfill(2)
    random_number = ''.join([str(random.randint(0, 9)) for _ in range(2)])
    matricule = f'{first_n}{last_n}{y}{m}{random_number}'
    return matricule

def listDoctors(request):
    doctors = DoctorProfile.objects.all()
    return render(request, 'planningmanager/listdoctors.html', {'doctors': doctors})


def saveAppointment(request):
    if request.method == 'POST':
        doctor = request.POST.get('doctor')
        date = request.POST.get('date')
        print('date:', date)
        mount = request.POST.get('mount')
        year =  request.POST.get('year')  
        print('year:', year)
        