from django.contrib import admin
from .models import Service_temp, Intervention_temp, DoctorProfile_temp, PatientProfile_temp, Appointment_temp, TimeSlot

# Register your models here.
class timeslotAdmin(admin.ModelAdmin):
    list_display = ('TimeSlot_day', 'doctor', 'slot_start', 'slot_end', 'patient_available', 'is_available')
    list_filter = ['TimeSlot_day','doctor', 'slot_start', 'patient_available', 'is_available']

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class serviceAdmin(admin.ModelAdmin):
    list_display = ('service_name', 'service_description')
    list_filter = ['service_name', 'service_description']
    readonly_fields=('id',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Service_temp)
admin.site.register(Intervention_temp)
admin.site.register(DoctorProfile_temp)
admin.site.register(PatientProfile_temp)
admin.site.register(Appointment_temp)
admin.site.register(TimeSlot, timeslotAdmin)