from django.contrib import admin
from .models import Service_temp, Intervention_temp, DoctorProfile_temp, PatientProfile_temp, Appointment_temp, TimeSlot

# Register your models here.
class timeslotAdmin(admin.ModelAdmin):
    list_display = ('id', 'slot_start','TimeSlot_day', 'doctor', 'patient_available', 'is_available')
    list_filter = ['TimeSlot_day','doctor', 'slot_start', 'patient_available', 'is_available']

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class serviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class InterventionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'service')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'doctorFullName', 'service', 'speciality')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class Appointment_tempAdmin(admin.ModelAdmin):
    list_display = ('appointment_id', 'patient', 'doctor', 'intervention', 'date_start', 'date_stop')
    list_filter = ('appointment_id', 'patient', 'doctor', 'intervention', 'date_added', 'date_start', 'date_stop')
    readonly_fields=('appointment_id',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Service_temp, serviceAdmin)
admin.site.register(Intervention_temp, InterventionAdmin)
admin.site.register(DoctorProfile_temp, DoctorProfileAdmin)
admin.site.register(PatientProfile_temp)
admin.site.register(Appointment_temp, Appointment_tempAdmin)
admin.site.register(TimeSlot, timeslotAdmin)