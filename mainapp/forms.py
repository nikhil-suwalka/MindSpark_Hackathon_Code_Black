from django import forms
from django.forms import Form, ModelForm, DateField, widgets
from .models import *

class UserForm(forms.ModelForm):


    class Meta:
        model = User1
        fields = ['first_name', 'last_name', 'email', 'address', 'city', 'state', 'pincode', 'phone', "license_no",
                  "qualification", "dob", "certificate", "type"]

        widgets = {
            'dob': widgets.DateInput(attrs={'type': 'date'})
        }
