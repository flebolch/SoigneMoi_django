from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save


# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, password=None):


        if not username:
            raise ValueError('User must have an username')

        user = self.model(
            username = self.normalize_email(username),
            first_name = first_name,
            last_name = last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, username, password):
            user = self.create_user(
                username = self.normalize_email(username),

                password = password,
                first_name = first_name,
                last_name = last_name,
            )
            user.is_admin = True
            user.is_staff = True
            user.is_active = True
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

    objects = MyAccountManager()

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
    service = models.CharField(max_length=30, blank=True)#, choices=SERVICE_CHOICES)
    speciality = models.CharField(max_length=30, blank=True)

    class Meta:
        verbose_name = 'doctor profile'
        verbose_name_plural = 'doctor profiles'

    def __str__(self):
        return self.user.username
    
    def full_name(self):
        return self.user.first_name.upper() + " " + self.user.last_name
    

class PatientProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, blank=True, null=True)
    address_line_1 = models.CharField(blank=True, max_length=100)
    address_line_2 = models.CharField(blank=True, max_length=100)
    city = models.CharField(blank=True, max_length=20)
    zipcode = models.CharField(blank=True, max_length=20)
    country = models.CharField(blank=True, max_length=20)

    class Meta:
        verbose_name = 'visitor profile'
        verbose_name_plural = 'visitor profiles'

    def __str__(self):
        return self.user.username

    def full_name(self):
        return self.user.first_name.upper() + " " + self.user.last_name

    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}' 



class SecretaryProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = 'secretary profile'
        verbose_name_plural = 'secretary profiles'

    def __str__(self):
        return self.user.username
    
    def full_name(self):
        return self.user.first_name.upper() + " " + self.user.last_name


class PlanningManagerProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = 'planning manager profile'
        verbose_name_plural = 'planning manager profiles'

    def __str__(self):
        return self.user.username
    
    def full_name(self):
        return self.user.first_name.upper() + " " + self.user.last_name