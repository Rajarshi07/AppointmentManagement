from django.contrib import admin
from .models import Appointment,AppointmentTypes

# Register your models here.

admin.site.register(Appointment)
admin.site.register(AppointmentTypes)