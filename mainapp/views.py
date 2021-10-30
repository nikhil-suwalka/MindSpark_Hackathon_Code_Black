from django.shortcuts import render
from .forms import *


# Create your views here.


def register(request):
    if request.method == "POST":
        user = User1.objects.create(first_name=request.POST["first_name"], last_name=request.POST["last_name"],
                                    license_no=request.POST["license_no"],
                                    address=request.POST["address"],
                                    city=request.POST["city"],
                                    state=request.POST["state"],
                                    pincode=request.POST["pincode"],
                                    phone=request.POST["phone"],
                                    qualification=request.POST["qualification"],
                                    dob=request.POST["dob"],
                                    certificate=request.FILES["certificate"],
                                    type=request.POST["type"],
                                    username=request.POST["license_no"],
                                    )
        user.save()

    register_form = UserForm(request.POST, request.FILES)
    context = {'register_form': register_form}
    return render(request, 'register.html', context)


def login(request):
    pass

def logout(request):
    pass