from django import forms
form ..models import Service

class DoctorFilterForm(forms.Form):
    service = forms.ModelChoiceField(queryset=Service.objects.all(), required=False)