from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='appointments_user_set',  # Add this line
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='appointments_user_set',  # Add this line
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100, default='General')
    # Add any other fields necessary for a doctor

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, default='N/A')
    address = models.CharField(max_length=255, default='Unknown')
    # Add any other fields necessary for a patient

class Slot(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    date = models.DateField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
