from django.contrib.auth import logout, authenticate, login
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
                                    username=request.POST["email"],
                                    email=request.POST["email"]
                                    )
        user.set_password(request.POST["password"])
        user.save()
        return render(request, 'login.html')

    register_form = RegisterForm(request.POST, request.FILES)
    context = {'register_form': register_form}
    return render(request, 'register.html', context)


def login_view(request):
    if request.method == "POST":

        user = authenticate(username=request.POST["email"], password=request.POST["password"])
        print(user, request.POST["password"], request.POST["email"])
        if not user:
            login_form = LoginForm(request.POST)
            return render(request, 'login.html', context={"message": "Invalid credentials", "login_form": login_form})

        else:
            login(request, user=user)
            return home(request)

    login_form = LoginForm(request.POST)
    context = {'login_form': login_form}

    return render(request, 'login.html', context)

def profile(request):
    pass


def logout_view(request):
    logout(request)
    return home(request)


def home(request):
    return render(request, 'index.html', context={"user": request.user})
