# appointments/urls.py
from django.urls import path
from .views import (
    DoctorRegisterView, PatientRegisterView, SlotAvailabilityView, SlotListView, 
    AppointmentBookingView, AppointmentCancellationView, AppointmentSearchView, UserAppointmentsView, SlotUpdateView, SlotDeleteView, PatientAppointmentHistoryView, DoctorAppointmentHistoryView, DoctorProfileView, PatientProfileView
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('doctors/register/', DoctorRegisterView.as_view(), name='doctor-register'),
    path('patients/register/', PatientRegisterView.as_view(), name='patient-register'),
    path('slots/declare/', SlotAvailabilityView.as_view(), name='slot-declare'),
    path('slots/', SlotListView.as_view(), name='slot-list'),
    path('slots/uodate/<int:pk>/', SlotUpdateView.as_view(), name='slot-update'),
    path('slots/delete/<int:pk>/', SlotDeleteView.as_view(), name='slot-delete'),
    path('appointments/book/', AppointmentBookingView.as_view(), name='appointment-book'),
    path('appointments/cancel/<int:pk>/', AppointmentCancellationView.as_view(), name='appointment-cancel'),
    path('appointments/search/', AppointmentSearchView.as_view(), name='appointment-search'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('appointments/', UserAppointmentsView.as_view(), name='user-appointments'),
    path('appointments/history/patient/', PatientAppointmentHistoryView.as_view(), name='patient-appointment-history'),
    path('appointments/history/doctor/', DoctorAppointmentHistoryView.as_view(), name='doctor-appointment-history'),
    path('profile/doctor/', DoctorProfileView.as_view(), name='doctor-profile'),
    path('profile/patient/', PatientProfileView.as_view(), name='patient-profile'),
]

