from django import forms
from django.forms import Form, ModelForm, DateField, widgets
from .models import *


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User1
        fields = ['first_name', 'last_name', 'email', "password", 'address', 'city', 'state', 'pincode', 'phone',
                  "license_no",
                  "qualification", "dob", "certificate", "type"]

        widgets = {
            'dob': widgets.DateInput(attrs={'type': 'date'})
        }


class LoginForm(forms.ModelForm):
    class Meta:
        model = User1
        fields = ['email', "password"]


class ProfileForm(forms.ModelForm):
    email = forms.CharField(disabled=True)
    license_no = forms.CharField(disabled=True)

    class Meta:
        model = User1
        fields = ['email', "password", "license_no", "first_name", "last_name", "address", "pincode", "city", "state",
                  "qualification", "dob"]
