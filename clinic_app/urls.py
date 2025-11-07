# clinic_app/urls.py


from django.urls import path, include  # ← Add include here
from . import views



urlpatterns = [
    # General Routes
    path('', views.home, name='home'),
    


    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    
    # Patient Routes
    path('patient/dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('patient/book/', views.book_appointment, name='book_appointment'),
    path('register/', views.patient_register, name='patient_register'), #
    # Doctor Route
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('doctor_register/', views.doctor_register, name='doctor_register'),
    # Admin is mostly handled by Django's default /admin/
    #   

]