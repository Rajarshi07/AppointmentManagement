from django.contrib import admin

# Register your models here.

from .models import DoctorProfile,PatientProfile
# Register your models here.
admin.site.register(DoctorProfile)
admin.site.register(PatientProfile)
