from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save
from django.utils import timezone
from datetime import time, timedelta
from django.utils.text import slugify


class Service(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'service'
        verbose_name_plural = 'services'

    def __str__(self):
        return self.name
      

class DoctorManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, password=None):


        if not username:
            raise ValueError('Vous devez avoir un email pour vous inscrire')

        user = self.model(
            username = self.normalize_email(username),
            first_name = first_name,
            last_name = last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

  
class Account(AbstractBaseUser):
    first_name      =models.CharField(max_length=50)
    last_name       =models.CharField(max_length=50)
    username        =models.CharField(max_length=150, unique=True)

    #required
    date_joined     =models.DateTimeField(auto_now_add=True)
    last_login      =models.DateTimeField(auto_now_add=True)
    is_admin        =models.BooleanField(default=False)
    is_staff        =models.BooleanField(default=False)
    is_active       =models.BooleanField(default=False)

   
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS =[ 'first_name','last_name']

    objects = DoctorManager()

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True


class DoctorProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, blank=True, null=True)
    service = models.ForeignKey(Service, on_delete=models.DO_NOTHING, blank=True, null=True, unique=False)
    speciality = models.CharField(max_length=30, blank=False)
    matricule = models.CharField(max_length=30, blank=False, unique=True)
    password_temp = models.CharField(max_length=30, blank=False)
    slug = models.SlugField(max_length=30, blank=True, unique=True)

    class Meta:
        verbose_name = 'doctor profile'
        verbose_name_plural = 'doctor profiles'

    def __str__(self):
        return self.full_name()
    
    # def __str__(self):
    #     return self.service.name
    
    def full_name(self):
        return self.user.first_name.upper() + " " + self.user.last_name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.matricule)
        super().save(*args, **kwargs)
    
# booking final model 
class TimeSlot(models.Model):
    def get_default_start_time():
        return timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)

    slot_start = models.DateTimeField(default=get_default_start_time, blank=False, null=False)
    slot_end = models.DateTimeField(blank=True, null=True)
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    patient_available = models.IntegerField(default=5)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'time_slot'
        verbose_name_plural = 'time_slots'

    class Meta:
        unique_together = ('doctor', 'slot_start')

    def __str__(self):
        return f"TimeSlot {self.slot_start} - {self.slot_end}"
        
    
    def __str__(self):
        return f"TimeSlot {self.slot_start} - {self.slot_end}, Doctor: {self.doctor.full_name()}"
    
    def save(self, *args, **kwargs):
        # Set slot_end to the end of the day
        if not self.slot_end:
            self.slot_end = self.slot_start.replace(hour=23, minute=59, second=59)
        super().save(*args, **kwargs)
    
    