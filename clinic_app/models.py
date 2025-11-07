

# Create your models here.
# clinic_app/models.py

from django.db import models
from django.contrib.auth.models import User

# --- 1. Extend User for Roles ---
class UserProfile(models.Model):
    USER_ROLES = (
        ('ADMIN', 'Admin'),
        ('DOCTOR', 'Doctor'),
        ('PATIENT', 'Patient'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=USER_ROLES)

    def __str__(self):
        return f"{self.user.username} ({self.role})"

# --- 2. Doctor Model ---
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)

    def __str__(self):
        return f"Dr. {self.user.first_name} ({self.specialization})"

# --- 3. Patient Model ---
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Patient: {self.user.first_name}"

# --- 4. Appointment Model (Integration) ---
class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    reason = models.TextField()
    status_choices = (
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
    )
    status = models.CharField(max_length=10, choices=status_choices, default='PENDING')

    def __str__(self):
        return f"Appt on {self.appointment_date.date()} - {self.status}"

        # doctors/models.py

# from django.db import models

# class Doctor(models.Model):
#     name = models.CharField(max_length=100)
#     specialization = models.CharField(max_length=100)
#     license_number = models.CharField(max_length=50, unique=True)
#     phone = models.CharField(max_length=20)
#     email = models.EmailField(unique=True)
#     is_active = models.BooleanField(default=True)
#     registration_date = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name + " (" + self.specialization + ")"


        


