from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class SexChoices(models.TextChoices):
    MALE = "Male", 'Male'
    FEMALE = "Female", 'Female'
    OTHERS = "Others", 'Others'

class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='patient')
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(max_length=17,validators=[phone_regex], blank=True)
    address = models.CharField(max_length=200,blank=True,default="")
    dob = models.DateField(blank=True)
    sex = models.TextField(max_length=10,choices=SexChoices.choices,blank=True)
    history = models.CharField(max_length=300,blank=True,default="")
    def __str__(self):  
        return self.user.get_full_name()
@receiver(post_save, sender=PatientProfile, dispatch_uid="set_user_patient")
def patient_postsave(sender, instance, **kwargs):
    Group.objects.get_or_create(name = 'patient')[0].user_set.add(instance.user)


class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='doctor')
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(max_length=17,validators=[phone_regex], blank=True)
    qualifications = models.CharField(max_length=70, blank=True,default="") 
    def __str__(self):
        return self.user.get_full_name()
@receiver(post_save, sender=DoctorProfile, dispatch_uid="set_user_doctor")
def doctor_postsave(sender, instance, **kwargs):
    Group.objects.get_or_create(name = 'doctor')[0].user_set.add(instance.user)
