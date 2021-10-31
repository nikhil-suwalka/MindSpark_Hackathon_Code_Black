from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(User1)
admin.site.register(Patient)
admin.site.register(Prescription)
admin.site.register(Medicine)
admin.site.register(MedicinePrescription)
admin.site.register(OTP)
admin.site.register(MedicineCsv)
