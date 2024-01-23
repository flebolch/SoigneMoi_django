from django.shortcuts import render, redirect, get_object_or_404
from .forms.registerationforms import RegistrationForm, PatientProfileForm
from .models import Account, PatientProfile
from django.contrib import messages, auth
from django.contrib.auth import authenticate, login

# Create your views here.
def register (request):
    if request.method == 'POST':
       form = RegistrationForm(request.POST)
       if form.is_valid():
           username = form.cleaned_data['username']
           first_name = form.cleaned_data['first_name']
           last_name = form.cleaned_data['last_name']
           password = form.cleaned_data['password']
           user = Account.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password)
           user.is_active = True
           print(user)
           user.save()
           PatientProfile.objects.create(user=user)
           return redirect('connection')
       else:
            print(f"Form errors: {form.errors}")
            print(f"Form errors: {form.non_field_errors}")
    else:
        print("problème de formulaire")
        form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'usermanager/register.html', context)

def login (request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            if user.is_active:
                print("Utilisateur actif")
            print("Authentification réussie")
            auth.login(request, user)
            if hasattr(user, 'patientprofile'):  # Check if the user has a PatientProfile
                if user.patientprofile.address_line_1 == '':  # Check if address_line_1 is empty
                    return edit_profile(request)
                else:
                    return visitordashboard(request)
            else:
                print("User does not have a PatientProfile")
                return redirect('visitordashboard')
        else:
            print("Problème d'authentification")
    else:
        print("Problème de méthode")
    return render(request, 'usermanager/login.html')

def edit_profile(request):
    # userprofile = get_object_or_404(UserProfile, user=request.user)
    # if request.method == 'POST':
    #     user_form = UserForm(request.POST, instance=request.user)
    #     profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
    #     if user_form.is_valid() and profile_form.is_valid():
    #         user_form.save()
    #         profile_form.save()
    #         messages.success(request, 'Your profile has been updated.')
    #         return redirect('edit_profile')
    # else:
    #     user_form = UserForm(instance=request.user)
    #     profile_form = UserProfileForm(instance=userprofile)
    # context = {
    #     'user_form': user_form,
    #     'profile_form': profile_form,
    #     'userprofile': userprofile,
    # }
    return render(request, 'usermanager/patient_info.html')


def visitordashboard (request):
    return render(request, 'usermanager/mon_espace_visiteur.html')


def logout (request):
    return

