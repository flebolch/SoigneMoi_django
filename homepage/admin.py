from django.contrib import admin
from .models import Service, Intervention, Doctor_TMP

# Register your models here.
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'short_description')
    prepopulated_fields = {'slug': ('name',)}

    def short_description(self, obj):
        return obj.description[:30]
    short_description.short_description = 'Description'

class InterventionAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration', 'service', 'short_description')
    list_filter = ('service',)
    search_fields = ('name', 'service__name')

    def short_description(self, obj):
        return obj.description[:30]
    
# Class TMP 
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'qualification', 'service')
    list_filter = ('service',)
    search_fields = ('fullname', 'service__name')



admin.site.register(Service, ServiceAdmin)
admin.site.register(Intervention, InterventionAdmin)
admin.site.register(Doctor_TMP, DoctorAdmin)
admin.site.site_header = 'Administration de la clinique'