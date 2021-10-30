import random

from django.contrib.auth import logout, authenticate, login
from django.core.mail import send_mail
from django.shortcuts import render

from .forms import *


# Create your views here.


def register(request):
    register_form = RegisterForm(request.POST, request.FILES)
    if request.method == "POST":
        if User1.objects.filter(email=request.POST["email"]).all() is not None:
            return render(request, 'register.html',
                          context={"message": "Email already exists in the system", "register_form": register_form})
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
        login_form = LoginForm(request.POST)
        return render(request, 'login.html', {"login_form": login_form})

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
    if request.method == "POST":
        # updated some entries in profile
        user = User1.objects.get(pk=request.user.license_no)
        user.first_name = request.POST["first_name"]
        user.last_name = request.POST["last_name"]
        user.address = request.POST["address"]
        user.pincode = request.POST["pincode"]
        user.city = request.POST["city"]
        user.state = request.POST["state"]
        user.qualification = request.POST["qualification"]
        user.dob = request.POST["dob"]
        user.save()

    user = User1.objects.filter(pk=request.user.license_no).get()
    profile_form = ProfileForm(request.POST)
    # print(request.user.license_no)
    user_dict = user.__dict__
    context = {'profile_form': profile_form, 'user_dict': user_dict}

    return render(request, 'profile.html', context)


def logout_view(request):
    logout(request)
    return home(request)


def home(request):
    return render(request, 'index.html', context={"user": request.user})


def prescribe(request):
    pass


def generateOTP():
    return random.randint(100000, 999999)


def aadhar(request):
    context = {'aadhar_form': AadharForm(request.POST)}

    if request.method == "POST":
        otp = generateOTP()
        print(request.POST["aadhar_no"])
        otp_object = OTP.objects.filter(aadhar=request.POST["aadhar_no"]).first()
        request.session['aadhar'] = request.POST["aadhar_no"]
        if otp_object:
            otp_object.otp = otp
            otp_object.save()
        else:
            OTP.objects.create(aadhar=request.POST["aadhar_no"], otp=otp)

        patient = Patient.objects.filter(aadhar_no=request.POST["aadhar_no"]).first()
        if patient:
            send_mail(
                'Prescription Portal : OTP request',
                "Your OTP is: " + str(otp),
                request.user.email,
                [patient.email],
                fail_silently=False,
            )
        else:
            context["message"] = "Invalid Aadhar Number"
            return render(request, 'aadhar_number_request_patient.html', context)

        return render(request, "request_otp.html",
                      context={"aadhar": request.POST["aadhar_no"], "otp_form": OTPForm(request.POST)})

    return render(request, 'aadhar_number_request_patient.html', context)


def aadhar_otp(request):
    otp = OTP.objects.filter(aadhar=request.POST["aadhar"]).first().otp
    print(request.POST, otp)
    request.session["otp"] = request.POST["otp"]
    if request.POST["otp"] == str(otp):
        patient_ob = Patient.objects.filter(aadhar_no=request.POST["aadhar"]).first()
        patient_name = patient_ob.first_name + " " + patient_ob.last_name

        return render(request, "patient_pharma_prescriptions.html",
                      context={"aadhar": request.POST["aadhar"],
                               "prescriptions": getPrescriptions(request.POST["aadhar"]),
                               "patient_name": patient_name
                               })
    else:
        return render(request, "request_otp.html",
                      context={"Message": "Incorrect OTP", "aadhar": request.POST["aadhar"],
                               "otp_form": OTPForm(request.POST)})


def getPrescriptions(aadhar_no):
    patient = Patient.objects.filter(aadhar_no=aadhar_no).first()
    prescriptions = Prescription.objects.filter(patient_id=patient.id).all()
    arr = []
    for prescription in prescriptions:
        dict1 = {"prescription_id": prescription.id, "date": prescription.date.strftime("%d/%m/%Y"),
                 "allowed_frequency": prescription.allowed_frequency, "given": prescription.given}
        doc = User1.objects.filter(email=prescription.doctor_id).get()
        dict1["doctor_name"] = doc.first_name + " " + doc.last_name

        arr.append(dict1)
    return arr


def getMedicinesFromPrescription(prescription_id):
    medicines = MedicinePrescription.objects.filter(pres_id=prescription_id).all()
    arr = []
    for medicine in medicines:
        dict1 = {"quantity": medicine.quantity}
        print(medicine.medicine_id)
        current_medicine = Medicine.objects.filter(pk=medicine.medicine_id.pk).get()
        dict1["name"] = current_medicine.name
        dict1["type"] = current_medicine.type
        arr.append(dict1)

    return arr


def prescription(request, p_id):
    user_type = request.user.type

    return render(request, "patient_pharma_prescription.html",
                  context={
                      "prescription": getMedicinesFromPrescription(p_id), "prescription_id": p_id,
                      "user_type": user_type
                  })


def order_complete(request, p_id):
    p = Prescription.objects.filter(pk=p_id).get()
    p.given = True
    p.save()

    patient_ob = Patient.objects.filter(aadhar_no=request.POST["aadhar"]).first()
    patient_name = patient_ob.first_name + " " + patient_ob.last_name

    return render(request, "patient_pharma_prescriptions.html",
                  context={"aadhar": request.session["aadhar"],
                           "prescriptions": getPrescriptions(request.session["aadhar"]),
                           "patient_name": patient_name})
