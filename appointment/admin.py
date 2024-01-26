from django.contrib import admin
from .models import Service_temp, Intervention_temp, DoctorProfile_temp, PatientProfile_temp, Appointment

# Register your models here.
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)

class InterventionAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration', 'service')
    list_filter = ('name', 'duration', 'service')

class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ('doctorFullName', 'service', 'speciality')
    list_filter = ('doctorFullName', 'service', 'speciality')

class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ('patientFullName', 'full_address')
    list_filter = ('patientFullName', 'full_address')

class appointmentAdmin(admin.ModelAdmin):
    list_display = ('appointment_id', 'patient', 'doctor', 'intervention', 'date_added', 'date_start', 'date_stop')
    list_filter = ('appointment_id', 'patient', 'doctor', 'intervention', 'date_added', 'date_start', 'date_stop')

admin.site.register(Service_temp, ServiceAdmin)
admin.site.register(Intervention_temp, InterventionAdmin)
admin.site.register(DoctorProfile_temp, DoctorProfileAdmin)
admin.site.register(PatientProfile_temp, PatientProfileAdmin)
admin.site.register(Appointment, appointmentAdmin)
