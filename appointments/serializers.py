# appointments/serializers.py
from rest_framework import serializers
from .models import Doctor, Patient, Slot, Appointment, User
from django.contrib.auth.models import user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_doctor', 'is_patient', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_doctor=validated_data['is_doctor'],
            is_patient=validated_data['is_patient']
        )
        return user

class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Doctor
        fields = ['id', 'user', 'specialization', 'phone_number', 'address']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        doctor = Doctor.objects.create(user=user, specialization=validated_data['specialization'])
        return doctor

class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Patient
        fields = ['id', 'user', 'phone_number', 'address']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        patient = Patient.objects.create(user=user, phone_number=validated_data['phone_number'], address=validated_data['address'])
        return patient

class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = ['id', 'start_time', 'end_time', 'date', 'doctor', 'is_available']

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'slot', 'is_active']
