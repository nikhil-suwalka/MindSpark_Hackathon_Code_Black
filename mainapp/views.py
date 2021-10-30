from django.shortcuts import render
from .forms import *

# Create your views here.


def register(request):
    register_form = UserForm(request.POST)
    context = {'register_form': register_form}
    return render(request, 'register.html', context)