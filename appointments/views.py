# appointments/views.py
from rest_framework import generics, status, viewsets, serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from .models import Doctor, Patient, Slot, Appointment
from .serializers import DoctorSerializer, PatientSerializer, SlotSerializer, AppointmentSerializer
from datetime import datetime

class DoctorRegisterView(generics.CreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class PatientRegisterView(generics.CreateAPIView):  # Add this class
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class BulkSlotSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        slots = [Slot(**item) for item in validated_data]
        return Slot.objects.bulk_create(slots)

class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = '__all__'
        list_serializer_class = BulkSlotSerializer

class SlotAvailabilityView(generics.CreateAPIView):
    queryset = Slot.objects.all()
    serializer_class = SlotSerializer
    permission_classes = [IsAuthenticated]

class SlotListView(generics.ListAPIView):
    serializer_class = SlotSerializer

    def get_queryset(self):
        return Slot.objects.filter(is_available=True).order_by('date', 'start_time')

class AppointmentBookingView(generics.CreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        patient_id = request.data.get('patient')
        slot_id = request.data.get('slot')
        slot = Slot.objects.get(id=slot_id)
        
        # Check if the slot is available
        if not slot.is_available:
            return Response({"error": "Slot is not available"}, status=status.HTTP_400_BAD_REQUEST)

        # Check for double booking
        existing_appointments = Appointment.objects.filter(patient_id=patient_id, slot__date=slot.date, slot__start_time=slot.start_time)
        if existing_appointments.exists():
            return Response({"error": "You already have an appointment at this time"}, status=status.HTTP_400_BAD_REQUEST)
        
        slot.is_available = False
        slot.save()
        return super().create(request, *args, **kwargs)

class AppointmentCancellationView(generics.DestroyAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        appointment = self.get_object()
        slot = appointment.slot
        slot.is_available = True
        slot.save()
        return super().destroy(request, *args, **kwargs)

class AppointmentSearchView(generics.ListAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        doctor_name = self.request.query_params.get('doctor_name')
        patient_name = self.request.query_params.get('patient_name')
        date = self.request.query_params.get('date')
        time = self.request.query_params.get('time')

        queryset = Appointment.objects.all()

        if doctor_name:
            queryset = queryset.filter(slot__doctor__user__username__icontains=doctor_name)
        if patient_name:
            queryset = queryset.filter(patient__user__username__icontains=patient_name)
        if date:
            try:
                date_obj = datetime.strptime(date, '%Y-%m-%d').date()
                queryset = queryset.filter(slot__date=date_obj)
            except ValueError:
                pass
        if time:
            try:
                time_obj = datetime.strptime(time, '%H:%M:%S').time()
                queryset = queryset.filter(slot__start_time__lte=time_obj, slot__end_time__gte=time_obj)
            except ValueError:
                pass

        return queryset

class UserAppointmentsView(ListAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'doctor'):
            return Appointment.objects.filter(slot__doctor=user.doctor)
        elif hasattr(user, 'patient'):
            return Appointment.objects.filter(patient=user.patient)
        return Appointment.objects.none()
    
class SlotUpdateView(generics.UpdateAPIView):
    queryset = Slot.objects.all()
    serializer_class = SlotSerializer
    permission_classes = [IsAuthenticated]

class SlotDeleteView(generics.DestroyAPIView):
    queryset = Slot.objects.all()
    serializer_class = SlotSerializer
    permission_classes = [IsAuthenticated]

class PatientAppointmentHistoryView(ListAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'patient'):
            return Appointment.objects.filter(patient=user.patient).order_by('-slot__date', '-slot__start_time')
        return Appointment.objects.none()
    
class DoctorAppointmentHistoryView(ListAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'doctor'):
            return Appointment.objects.filter(slot__doctor=user.doctor).order_by('-slot__date', '-slot__start_time')
        return Appointment.objects.none()
    
class DoctorProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.doctor

class PatientProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.patient