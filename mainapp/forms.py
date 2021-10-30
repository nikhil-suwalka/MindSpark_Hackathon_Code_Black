from django import forms

from .models import *


class UserForm(forms.ModelForm):

    class Meta:
        model = User1
        fields = ['first_name', 'last_name', 'email', 'address', 'city', 'state', 'pincode', 'phone', "license_no",
                  "qualification", "dob", "certificate", "type"]
