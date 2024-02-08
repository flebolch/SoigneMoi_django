from django import forms
from ..models import Account, PatientProfile

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Mot de passe',
        'class': 'form-control',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirmer le mot de passe',
        'class': 'form-control',
    }))

    username = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Adresse email',
        'class': 'form-control',
    }))

    class Meta:
        model = Account
        fields = ( 'username', 'first_name', 'last_name','password')

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        username = cleaned_data.get('email')
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if Account.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "L'adresse email existe déjà"
            )

        if password != confirm_password:
            raise forms.ValidationError(
                "Les mots de passe ne correspondent pas"
            )
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Adresse email'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Nom d\'utilisateur'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Prénom d\'utilisateur'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class PatientProfileForm(forms.ModelForm):
    model  = PatientProfile
    fields = ('address_line_1', 'address_line_2', 'city', 'zipcode', 'country')

    def __init__(self, *args, **kwargs):
        super(PatientProfileForm, self).__init__(*args, **kwargs)
        self.fields['address_line_1'].widget.attrs['placeholder'] = 'Adresse ligne 1'
        self.fields['address_line_2'].widget.attrs['placeholder'] = 'Adresse ligne 2'
        self.fields['city'].widget.attrs['placeholder'] = 'Ville'
        self.fields['zipcode'].widget.attrs['placeholder'] = 'Code postal'
        self.fields['country'].widget.attrs['placeholder'] = 'Pays'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'