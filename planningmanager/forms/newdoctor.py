from django import forms    
from ..models import Account, DoctorProfile, Service
from ..models import Service



class DoctorForm(forms.ModelForm):
    service = forms.ModelChoiceField(queryset=Service.objects.all(), widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Choisissez un service'}))
    matricule = forms.CharField(required=False)
    password_temp = forms.CharField(required=False)
    class Meta:
        model = DoctorProfile
        fields = ['user', 'service', 'speciality', 'matricule', 'password_temp']
        widgets = {
            'speciality': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def clean_matricule(self):
        matricule = self.cleaned_data.get('matricule')
        if not matricule:
            matricule = 'matriculeTMP'
        return matricule
       
    def __init__(self, *args, **kwargs):
        super(DoctorForm, self).__init__(*args, **kwargs)
        self.fields['service'].widget.attrs['placeholder'] = 'choisissez un service'
        self.fields['speciality'].widget.attrs['placeholder'] = 'Spécialité'
        self.fields['matricule'].initial = 'matriculeTMP'


class AccountForm(forms.ModelForm):
    password = forms.CharField(required=False)
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
        self.fields['password'].initial = 'P*ssw0rdTMP123'
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:    
            password = 'P*ssw0rdTMP123'
        return password
    
    def clean(self):
        cleaned_data = super(AccountForm, self).clean()
        username = cleaned_data.get('username')
        if Account.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "L'adresse email est déja utilisée."
            ) 

