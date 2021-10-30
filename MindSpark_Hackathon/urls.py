"""MindSpark_Hackathon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from mainapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('register/', register, name="register"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('profile/', profile, name="profile"),
    path('orders/', aadhar, name="orders"),
    path('orders/otp', aadhar_otp, name="aadhar_otp"),
    path('orders/prescriptions/<int:p_id>', prescription, name="prescription"),
    path('orders/complete/<int:p_id>', order_complete, name="order_complete"),
    path('prescribe/', aadhar, name="prescribe"),
    path('prescribe/list', aadhar_otp, name="prescribe_list"),
    path('prescribe/create', prescription_create, name="prescription_create"),
    path('prescribe/create/<int:p_id>', prescription_create_with_id, name="prescription_create_with_id"),
    path('prescribe/delete/<int:p_id>', prescription_delete_with_id, name="prescription_delete_with_id"),
    path('add_medicines/', add_medicines_csv, name="add_medicines"),
    path('add_medicines_from_csv/', add_medicines_from_csv_view, name="add_medicines_from_csv_view"),
]
