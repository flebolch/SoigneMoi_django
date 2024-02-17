from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save
from django.utils import timezone
from datetime import time, timedelta

# Create your models here.

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
    service = models.CharField(max_length=30, blank=True)
    speciality = models.CharField(max_length=30, blank=False)
    matricule = models.CharField(max_length=30, blank=False, unique=True)
    password_temp = models.CharField(max_length=30, blank=False)

    class Meta:
        verbose_name = 'doctor profile'
        verbose_name_plural = 'doctor profiles'

    def __str__(self):
        return self.user.username
    
    def full_name(self):
        return self.user.first_name.upper() + " " + self.user.last_name
    
# Create your models here.
class Service_temp(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'service'
        verbose_name_plural = 'services'

    def __str__(self):
        return self.name
    