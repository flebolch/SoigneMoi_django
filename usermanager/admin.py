from django.contrib import admin
from .models import Account, DoctorProfile,PatientProfile, SecretaryProfile, PlanningManagerProfile
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'date_joined', 'last_login','is_active')
    search_fields = ('email', 'first_name', 'last_name')
    readonly_fields = ('date_joined', 'last_login')
    ordering = ('-date_joined',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class DoctorProfileAdmin(admin.ModelAdmin):
    list_display =['full_name','speciality', 'service']

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class PatientProfileAdmin(admin.ModelAdmin):
    list_display =( 'user', 'full_name', 'full_address', 'city', 'zipcode', 'country')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class SecretaryProfileAdmin(admin.ModelAdmin):
    list_display =( 'user', 'full_name')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class PlanningManagerProfileAdmin(admin.ModelAdmin):
    list_display =( 'user', 'full_name')
    filter_horizontal = ()
    list_filter = ()


admin.site.register(Account, AccountAdmin)
admin.site.register(DoctorProfile, DoctorProfileAdmin )
admin.site.register(PatientProfile, PatientProfileAdmin)
admin.site.register(SecretaryProfile, SecretaryProfileAdmin)
admin.site.register(PlanningManagerProfile, PlanningManagerProfileAdmin)