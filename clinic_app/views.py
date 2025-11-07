# clinic_app/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from .models import UserProfile, Doctor, Patient, Appointment
from .forms import DoctorRegistrationForm

# ------------------------------------------------
# Helper Functions for Role Checking
# ------------------------------------------------
def is_patient(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'PATIENT'

def is_doctor(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'DOCTOR'


# ------------------------------------------------
# Home / Login / Logout
# ------------------------------------------------
def home(request):
    if request.user.is_authenticated:
        # Redirect based on role
        if not hasattr(request.user, 'userprofile'):
            return render(request, 'home.html', {'error': 'No user profile found for this account.'})

        role = request.user.userprofile.role
        if role == 'ADMIN':
            return redirect('/admin/')
        elif role == 'DOCTOR':
            return redirect('doctor_dashboard')
        elif role == 'PATIENT':
            return redirect('patient_dashboard')
    return render(request, 'home.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect based on role
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect('home')


# ------------------------------------------------
# Patient Registration and Views
# ------------------------------------------------
def patient_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')

        # 1️⃣ Create base user
        new_user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name)

        # 2️⃣ Create user profile
        UserProfile.objects.create(user=new_user, role='PATIENT')

        # 3️⃣ Create patient record
        Patient.objects.create(user=new_user)

        # 4️⃣ Auto login
        login(request, new_user)
        return redirect('patient_dashboard')

    return render(request, 'patient_register.html')


# @login_required
# @user_passes_test(is_patient)
# def patient_dashboard(request):
#     patient_profile = request.user.patient
#     appointments = Appointment.objects.filter(patient=patient_profile).order_by('appointment_date')
#     return render(request, 'patient_dashboard.html', {'appointments': appointments})

# clinic_app/views.py

# Ensure you have imported the Patient model at the top:
# from .models import UserProfile, Doctor, Patient, Appointment 
# (It looks like you already have this)

# ... (other view functions)

@login_required
@user_passes_test(is_patient)
def patient_dashboard(request):
    """
    Displays the patient's dashboard.
    Includes error handling for missing Patient profiles (RelatedObjectDoesNotExist).
    """
    user = request.user
    
    try:
        # Attempt to get the patient profile
        patient_profile = user.patient
    except Patient.DoesNotExist:
        # If the Patient object is missing (but UserProfile says they are a patient),
        # create the missing profile defensively.
        # This addresses the User has no patient. error.
        patient_profile = Patient.objects.create(user=user)
        
    # Continue with dashboard logic using the guaranteed patient_profile object
    appointments = Appointment.objects.filter(patient=patient_profile).order_by('appointment_date')
    return render(request, 'patient_dashboard.html', {'appointments': appointments})

# ... (other view functions)


@login_required
@user_passes_test(is_patient)
def book_appointment(request):
    doctors = Doctor.objects.all()
    if request.method == 'POST':
        patient_profile = request.user.patient
        doctor_id = request.POST.get('doctor_id')
        appt_datetime = request.POST.get('appointment_date')
        reason = request.POST.get('reason')

        selected_doctor = Doctor.objects.get(id=doctor_id)

        Appointment.objects.create(
            patient=patient_profile,
            doctor=selected_doctor,
            appointment_date=appt_datetime,
            reason=reason
        )
        return redirect('patient_dashboard')

    return render(request, 'book_appointment.html', {'doctors': doctors})


# ------------------------------------------------
# Doctor Registration and Views
# ------------------------------------------------
def doctor_register(request):
    if request.method == 'POST':
        form = DoctorRegistrationForm(request.POST)
        if form.is_valid():
            # 1️⃣ Create base user
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )

            # 2️⃣ Create user profile for DOCTOR
            UserProfile.objects.create(user=user, role='DOCTOR')

            # 3️⃣ Create doctor record
            Doctor.objects.create(
                user=user,
                specialization=form.cleaned_data['specialization']
            )

            return redirect('user_login')
    else:
        form = DoctorRegistrationForm()

    return render(request, 'doctor_register.html', {'form': form})


@login_required
@user_passes_test(is_doctor)
def doctor_dashboard(request):
    doctor_profile = request.user.doctor
    appointments = Appointment.objects.filter(
        doctor=doctor_profile,
        appointment_date__gte=timezone.now()
    ).order_by('appointment_date')

    return render(request, 'doctor_dashboard.html', {'appointments': appointments})
