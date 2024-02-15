from django.contrib import admin
from .models import Account, DoctorProfile, Service_temp

# Register your models here.
class serviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'service', 'speciality', 'matricule', 'password_temp')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff', 'is_active')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Service_temp, serviceAdmin)
admin.site.register(DoctorProfile, DoctorProfileAdmin)
admin.site.register(Account, AccountAdmin)