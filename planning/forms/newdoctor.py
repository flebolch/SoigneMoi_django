from django import forms    
from ..models import Account, DoctorProfile, Service_temp
import random
from datetime import date

def GeneratePassordTemp():
    pwdlenght = 10
    characters = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()')
    temp_password = ''.join(random.choice(characters) for i in range(pwdlenght))
    return temp_password

def generateMatricule():
    current_date = date.today()
    rndchar = ''.join([str(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')) for _ in range(3)])
    y = str(current_date.year)[-2:]
    m = str(current_date.month).zfill(2)
    random_number = ''.join([str(random.randint(0, 9)) for _ in range(2)])
    matricule = f'{rndchar}{y}{m}{random_number}'
    return matricule

def choice_service():
    choice = Service_temp.objects.all()
    service_list = []
    for i in choice:
        service_list.append((i.id, i.name))
    return service_list

class DoctorForm(forms.ModelForm):
    service = forms.ChoiceField(widget=forms.Select, choices=choice_service())
    class Meta:
        model = DoctorProfile
        fields = ['user', 'service', 'speciality', 'matricule', 'password_temp']
        widgets = {
            'service': forms.ChoiceField(widget=forms.Select, choices=choice_service()),
            'speciality': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(DoctorForm, self).__init__(*args, **kwargs)
        self.fields['service'].widget.attrs['class'] = 'choisissez un service'
        self.fields['speciality'].widget.attrs['placeholder'] = 'Spécialité'
        self.initial['matricule'] = generateMatricule()

       

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        self.fields['last_name'].widget.attrs['placeholder'] = 'Nom'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Prénom'
        self.fields['username'].widget.attrs['placeholder'] = 'email'
        self.initial['password_temp'] = GeneratePassordTemp()
        
