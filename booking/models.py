from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from django.utils import timezone
from datetime import time, timedelta


# Create your models here.
class Service_temp(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'service'
        verbose_name_plural = 'services'

    def __str__(self):
        return self.name
    
class Intervention_temp(models.Model):
    name = models.CharField(max_length=100)
    duration = models.PositiveSmallIntegerField() 
    service = models.ForeignKey(Service_temp, blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'intervention'
        verbose_name_plural = 'interventions'

    def __str__(self) -> str:
        return f"{self.name} service: {self.service}"

class DoctorProfile_temp(models.Model):
    doctorFullName = models.CharField(max_length=100, blank=False, null=False)
    service = models.ForeignKey(Service_temp, on_delete=models.CASCADE)
    speciality = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.doctorFullName

class PatientProfile_temp(models.Model):
    patientFullName = models.CharField(max_length=100, blank=False, null=False)
    full_address = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.patientFullName

class Appointment_temp(models.Model):
    def get_default_start_time():
        return timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    def get_default_end_time():
        return timezone.now().replace(hour=23, minute=59, second=59, microsecond=0)
    
    appointment_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(PatientProfile_temp, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorProfile_temp, on_delete=models.CASCADE)
    intervention = models.ForeignKey(Intervention_temp, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    date_start = models.DateTimeField(default=get_default_start_time, blank=False, null=False)
    date_stop = models.DateTimeField(default=get_default_end_time, blank=False, null=False)


    def duration(self):
        return self.date_stop - self.date_start
    
    def save(self, *args, **kwargs):
        if self.date_start >= self.date_stop:
            raise ValidationError(_("date_start must be before date_stop"))
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'appointment'
        verbose_name_plural = 'appointments'

    def __str__(self):
        return str(self.appointment_id)
    
# booking final model 
class TimeSlot(models.Model):
    def get_default_start_time():
        return timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)

    slot_start = models.DateTimeField(default=get_default_start_time, blank=False, null=False)
    slot_end = models.DateTimeField(blank=True, null=True)
    doctor = models.ForeignKey(DoctorProfile_temp, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    patient_available = models.IntegerField(default=5)
    date_added = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Set slot_end to the end of the day
        if not self.slot_end:
            self.slot_end = self.slot_start.replace(hour=23, minute=59, second=59)
        super().save(*args, **kwargs)
    
    def TimeSlot_day(self):
        return self.slot_start.date()
    
    class Meta:
        verbose_name = 'time_slot'
        verbose_name_plural = 'time_slots'

    def __str__(self):
        return f"TimeSlot {self.slot_start} - {self.slot_end}"