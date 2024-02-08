from django.shortcuts import render, redirect, get_object_or_404
from .forms.registerationforms import RegistrationForm, PatientProfileForm
from .models import Account, PatientProfile
from django.contrib import messages, auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

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
           messages.success(request, 'Votre compte a été créé avec succès')
           return redirect('connection')
       else:
            for filed, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error, extra_tags='danger')
            return render(request, 'usermanager/register.html', {'form': form})
    else:
        form = RegistrationForm()
    return render(request, 'usermanager/register.html', {'form': form})

def login (request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                # case : User is a patient and has a completed profile
                if hasattr(user, 'patientprofile'):  # Check if the user has a PatientProfile
                    if user.patientprofile.address_line_1 != '':  # Check if address_line_1 is empty
                        return redirect('mon_espace_visiteur')
                    # case : User is visitor but has no profile
                    else:
                        return redirect('nouveau_visiteur')
                else:
                    messages.error(request, 'Votre compte n\'a pas de profile visiteur. Veuillez contacter l\'administrateur', extra_tags='danger')
                    auth.logout(request)
                    return redirect('connection')
        else:
            print("Problème d'authentification")
    else:
        print("Problème de méthode")
    return render(request, 'usermanager/login.html')

@login_required
def register_visitor(request):
    return render(request, 'usermanager/nouveau_visiteur.html')

@login_required
def visitordashboard (request):
    visitorprofile = get_object_or_404(PatientProfile, user=request.user)
    context = {
        'visitorprofile': visitorprofile
    }
    return render(request, 'usermanager/mon_espace_visiteur.html', context)

@login_required
def logout (request):
    auth.logout(request)
    messages.success(request, 'Vous êtes déconnecté')
    return redirect('connection')

