from django.db import models

# Create your models here.
class Service(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=500, blank=True)
    image = models.ImageField(upload_to='photos/services', blank=True)

    class Meta:
        verbose_name = 'service'
        verbose_name_plural = 'services'

    def __str__(self):
        return self.name


    
class Intervention(models.Model):
    name = models.CharField(max_length=100)
    duration = models.PositiveSmallIntegerField() 
    description = models.TextField(max_length=500, blank=True)
    service = models.ForeignKey(Service, blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'intervention'
        verbose_name_plural = 'interventions'

    def __str__(self):
        return self.name
    
class Doctor_TMP(models.Model):
    fullname = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100)
    service = models.ForeignKey(Service, blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Doctor_TMP'
        verbose_name_plural = 'Doctors_TMP'

    def __str__(self):
        return self.fullname
