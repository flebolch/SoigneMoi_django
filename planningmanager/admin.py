from django.contrib import admin
from .models import Account, DoctorProfile, Service, TimeSlot

# Register your models here.


class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'user', 'service',  'speciality', 'matricule', 'password_temp')
    prepopulated_fields = {'slug': ('matricule',)}

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff', 'is_active')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class serviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class timeslotAdmin(admin.ModelAdmin):
    list_display = ('id', 'slot_start', 'doctor', 'patient_available', 'is_available')
    list_filter = ['TimeSlot_day','doctor', 'slot_start', 'patient_available', 'is_available']

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()



admin.site.register(Service, serviceAdmin)
admin.site.register(DoctorProfile, DoctorProfileAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(TimeSlot, timeslotAdmin)