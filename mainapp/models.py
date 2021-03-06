from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class Patient(models.Model):
    first_name = models.CharField(blank=False, null=False, max_length=100)
    last_name = models.CharField(blank=False, null=False, max_length=100)
    aadhar_no = models.CharField(blank=False, null=False, max_length=100)
    phone_no = models.CharField(blank=False, null=False, max_length=100)
    email = models.EmailField(blank=False, null=False, max_length=100)
    dob = models.DateField(blank=False, null=False)
    gender = models.CharField(blank=False, null=False, max_length=100)
    address = models.CharField(blank=False, null=False, max_length=100)

    def __str__(self):
        return str(self.first_name)


class OTP(models.Model):
    aadhar = models.CharField(blank=False, null=False, primary_key=True, max_length=100)
    otp = models.IntegerField()


class User1(AbstractUser):
    license_no = models.CharField(blank=False, null=False, max_length=100, primary_key=True)
    address = models.CharField(blank=False, max_length=100, null=False, )
    city = models.CharField(blank=False, max_length=100, null=False, )
    state = models.CharField(blank=False, max_length=100, null=False, )
    pincode = models.IntegerField(blank=True, null=False, default=0)
    phone = models.CharField(blank=False, max_length=100, null=False, )
    qualification = models.CharField(blank=False, max_length=100, null=False, )
    dob = models.DateField(blank=True, null=False, default="1970-01-01")
    certificate = models.ImageField(upload_to="static", null=False, )
    TYPES = ((0, "Doctor"), (1, "Pharmacist"))
    type = models.IntegerField(default=1, choices=TYPES)
    approved = models.BooleanField(default=False)


class Medicine(models.Model):
    name = models.CharField(blank=False, null=False, max_length=100)
    type = models.CharField(blank=False, null=False, max_length=100)
    TYPES = ((0, "One time"), (1, "Multiple"))
    allowed_frequency = models.IntegerField(default=1, choices=TYPES)

    def __str__(self):
        return str(self.name)


class Prescription(models.Model):
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="prescription_patient_id")
    doctor_id = models.ForeignKey(User1, on_delete=models.CASCADE, related_name="prescription_doctor_id")
    date = models.DateTimeField(blank=False, null=False, auto_now_add=True)
    given = models.BooleanField(default=False)


class MedicinePrescription(models.Model):
    pres_id = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name="med_pres_prescription_id")
    medicine_id = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name="med_pres_medicine_id")
    quantity = models.IntegerField(blank=False, null=False)
    note = models.CharField(blank=True, null=True, max_length=100)


class MedicineCsv(models.Model):
    file = models.FileField(upload_to="medicine_csv", null=False)
    date = models.DateTimeField(blank=False, null=False, auto_now_add=True)
