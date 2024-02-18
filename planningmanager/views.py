from django.shortcuts import render, get_object_or_404
from .forms.newdoctor import DoctorForm, AccountForm
from .models import Account, DoctorProfile
from django.contrib import messages
import random
from datetime import date
from django.db import transaction
from django.contrib import messages
from django.db import IntegrityError
from .models import DoctorProfile


def planningdashboard(request, matricule=None):
    matricule = None

    if matricule != None:
        doctors = get_object_or_404(DoctorProfile, matricule=matricule)
        print('matricule is not none', doctors)
    else:
        doctors = DoctorProfile.objects.all()
        print('matricule is none')
    context = {
        'doctors': doctors
    }
    return render(request, 'planning/planningdashboard.html', context)


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
            return render(request, 'planning/newDoctorProfile.html', {'doctor_form': doctor_form, 'account_form': account_form})

        else:
            for field, errors in account_form.errors.items():
                for error in errors:
                    messages.error(request, error, extra_tags='danger')
            return render(request, 'planning/newDoctorProfile.html', {'doctor_form': doctor_form, 'account_form': account_form})
    else:

        context = {
            'doctor_form': DoctorForm(),
            'account_form': AccountForm()
        }
    return render(request, 'planning/newDoctorProfile.html', context)



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
    return render(request, 'planning/listdoctors.html', {'doctors': doctors})