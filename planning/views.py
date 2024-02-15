from django.shortcuts import render
from .forms.newdoctor import DoctorForm, AccountForm
from .models import Account, DoctorProfile
from django.contrib import messages


# Create your views here.
def planningdashboard(request):
    return render(request, 'planning/planning.html')

def doctorProfileAdmin(request):
    if request.method == 'POST':
        doctor_form = DoctorForm(request.POST)
        account_form = AccountForm(request.POST)
        if doctor_form.is_valid() and account_form.is_valid():
            user = account_form.save(commit=False)
            username = account_form.cleaned_data['username']
            first_name = account_form.cleaned_data['first_name']
            last_name = account_form.cleaned_data['last_name']
            password = doctor_form.cleaned_data['password_temp']
            user = Account.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password)
            print(user)
            user.is_active = True
            user.save()
            #create doctor
            profile = DoctorProfile()
            profile.user = user
            profile.service = doctor_form.cleaned_data['service']
            profile.speciality = doctor_form.cleaned_data['speciality']
            print(profile)
            profile.save()
            messages.success(request, 'Le médecin a été ajouté avec succès')
        else:
            print (doctor_form.errors)
            # print (account_form.errors)
    else:
        doctor_form = DoctorForm()
        account_form = AccountForm()
        
    return render(request, 'planning/doctorProfile.html', {'doctor_form': doctor_form, 'account_form': account_form})

# def GeneratePassordTemp():
#     pwdlenght = 10
#     characters = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()')
#     temp_password = ''.join(random.choice(characters) for i in range(pwdlenght))
#     return temp_password

# def generateMatricule(first_name, last_name):
#     current_date = date.today()
#     first_n = first_name[0]
#     last_n = last_name[0]
#     y = str(current_date.year)[-2:]
#     m = str(current_date.month).zfill(2)
#     random_number = ''.join([str(random.randint(0, 9)) for _ in range(2)])
#     matricule = f'{first_n}{last_n}{y}{m}{random_number}'
#     return matricule