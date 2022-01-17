from django.db import models
from users.models import PatientProfile,DoctorProfile
from django.utils import timezone
# Create your models here.

class AppointmentStatus(models.IntegerChoices):
    OPEN = 0, 'Open'
    BOOKED = 1, 'Booked'
    COMPLETED = 2, 'Completed'
    CANCELLED = 3, 'Cancelled'
    CHECKED_IN = 4, 'Checked In'
    MISSED = 5, 'Missed'

class PaymentStatus(models.IntegerChoices):
    DUE = 0, 'Due'
    PAID = 1, 'Paid'
    UNSET = 2, 'Unset'


## NOTES
# reminder if doctor reschedules, cancels or deletes appointment
# Amount,payment status //send mail on completion
# Type - Choices (to  be  given)
class Appointment(models.Model):
    doctor = models.ForeignKey(DoctorProfile, on_delete= models.CASCADE,related_name="doctor",null=True)
    status = models.IntegerField(choices=AppointmentStatus.choices,default=AppointmentStatus.OPEN)
    date = models.DateField(default=timezone.now)
    start_time = models.TimeField(blank=False)
    end_time = models.TimeField(blank=True,null=True)
    notes = models.CharField(max_length=300,blank=True,default="")
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE,blank=True,null=True,default=None,related_name="patient")
    apt_type = models.CharField(max_length=50,blank=True,default="")
    billing_amount = models.FloatField(default=0.00,blank=True)
    payment_status = models.IntegerField(choices=PaymentStatus.choices, default=PaymentStatus.UNSET)
    def save(self, *args, **kwargs):
        # overriding save method
        if self.status == AppointmentStatus.OPEN:
            self.notes=""
            self.patient=None
            self.apt_type=""
            self.billing_amount=0.00
            self.payment_status=PaymentStatus.UNSET
        super(Appointment, self).save(*args, **kwargs)
    def get_string_fields(self):
        return [
            ("doctor",self.doctor.user.get_full_name() if self.doctor else ""),
            ("date",self.date.strftime("%d-%m-%Y")),
            ("start_time",self.start_time.strftime("%I:%M %p") if self.start_time is not None else ""),
            ("end_time",self.end_time.strftime("%I:%M %p") if self.end_time is not None else ""),
            ("status",self.get_status_display()),
            ("patient",self.patient.user.get_full_name() if self.patient else ""),
            ("apt_type",self.apt_type),
            ("billing_amount",self.billing_amount),
            ("payment_status",self.get_payment_status_display),
            ("notes",self.notes),
        ]
    class Meta:
        ordering = ['date']
    def __str__(self):
        return self.doctor.user.get_full_name()+ " " + self.date.strftime("%d-%m-%Y") + " " + self.start_time.strftime("%H:%M") + " " + str(self.status)


class AppointmentTypes(models.Model):
    type = models.CharField(max_length=50,blank=True,default="")
    def __str__(self):
        return self.type