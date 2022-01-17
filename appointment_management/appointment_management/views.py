from os import stat_result
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import get_object_or_404, redirect,render
from django.contrib.auth.models import User,Group
from django.views.decorators.csrf import csrf_exempt
from webpush import send_user_notification,send_group_notification
import json
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from users.models import *
from users.utils import *
from appointments.models import *
from django.db.models import Q

@login_required
@require_GET
def home(request):
   data={}
   if is_user_doctor(request.user):
      doctor = DoctorProfile.objects.get(user=request.user)
      patients =  Appointment.objects.filter(doctor=doctor).values_list('patient', flat=True).distinct()
      data['appointments'] = Appointment.objects.filter((Q(doctor=DoctorProfile.objects.get(user=request.user)) & ~Q(status=AppointmentStatus.OPEN)))
      data['patients'] = PatientProfile.objects.filter(id__in=patients)
   elif is_user_patient(request.user):
      data['appointments'] = Appointment.objects.filter(patient=PatientProfile.objects.get(user=request.user))
      data['doctors']=DoctorProfile.objects.all()
   return render(request, 'home.html',data)
