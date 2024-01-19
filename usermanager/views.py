from django.shortcuts import render, redirect
from .forms.registerationforms import RegistrationForm
from .models import Account, PatientProfile

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
           print(user)
           user.save()
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
    return render(request, 'usermanager/login.html')

def logout (request):
    return

