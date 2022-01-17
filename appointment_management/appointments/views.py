from typing import overload
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render,redirect
from appointments.forms import appointmentForm,patientAppointmentForm
from users.models import DoctorProfile, PatientProfile
from users.utils import is_user_doctor, is_user_patient, sendnoti
from .models import Appointment,AppointmentStatus, AppointmentTypes,PaymentStatus
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.generic.list import ListView
from datetime import datetime
# from django.utils import timezone
from .email_utils import send_doctor_email, send_patient_email
from dateutil.rrule import rrule, DAILY
from datetime import date

# Create your views here.

class AppointmentsList(ListView):
    template_name = 'apt_list.html'
    model = Appointment
    context_object_name = 'object_list'
    ordering = ['start_time']
    def get_queryset(self):
        try:
            user = self.request.user
            date = self.request.GET.get('date', None)
            status = self.request.GET.get('status', None)
            doc = self.request.GET.get('doc', None)
            if is_user_patient(user):
                patient = PatientProfile.objects.get(user = user)
                appt= self.model.objects.filter((Q(patient=patient) | Q(status=AppointmentStatus.OPEN)))
                if doc:
                    appt = appt.filter(doctor=DoctorProfile.objects.get(pk = doc))
                if date:
                    date = datetime.strptime(date, '%Y-%m-%d').date()
                    appt = appt.filter(Q(date = date))
                if status == '0':
                    appt = appt.filter(Q(status = status) & Q(date__gte=datetime.today()))
                if status == '5':
                    appt.filter(Q(status = AppointmentStatus.BOOKED) & Q(date__lt=datetime.today())).update(status=AppointmentStatus.MISSED)
                    appt=appt.filter(Q(status = status))
                elif status:
                    appt = appt.filter(Q(status = status))
                else:
                    appt = appt.filter(Q(patient=patient) | Q(date__gte=datetime.today()))
                return appt
            elif is_user_doctor(user):
                doctor = DoctorProfile.objects.get(user = user)
                appt =  self.model.objects.filter(doctor=doctor)
                if date=='all':
                    pass
                elif date:
                    date = datetime.strptime(date, '%Y-%m-%d').date()
                    appt = appt.filter(Q(date = date))
                # else:
                #     appt = appt.filter(Q(date__gte=datetime.today()))
                if status == '0':
                    appt = appt.filter(Q(status = status) & Q(date__gte=datetime.today()))
                if status == '5':
                    appt.filter(Q(status = AppointmentStatus.BOOKED) & Q(date__lt=datetime.today())).update(status=AppointmentStatus.MISSED)
                    appt=appt.filter(Q(status = status))
                elif status:
                    appt = appt.filter(Q(status = status))
                else:
                    appt = appt.filter(Q(date__gte=datetime.today()))
                return appt
            else:
                return self.model.objects.filter(status=AppointmentStatus.OPEN)
        except Exception as e:
            print(e)
            return self.model.objects.filter(status=AppointmentStatus.OPEN)
    def get_context_data(self,**kwargs):
        context = super(AppointmentsList,self).get_context_data(**kwargs)
        status = self.request.GET.get('status', None)
        context['reschedule'] = self.request.GET.get('reschedule', None)
        context['apttype'] = AppointmentTypes.objects.all()
        if is_user_patient(self.request.user):
            doc = self.request.GET.get('doc', None)
            patient = PatientProfile.objects.get(user = self.request.user)
            if doc:
                context['aptdate'] = self.model.objects.filter((Q(patient=patient) | Q(status=AppointmentStatus.OPEN)) & Q(doctor=DoctorProfile.objects.get(pk = doc)))
            else:
                context['aptdate'] = self.model.objects.filter((Q(patient=patient) | Q(status=AppointmentStatus.OPEN)))
            context['doctors'] = DoctorProfile.objects.all()
        elif is_user_doctor(self.request.user):
            context['aptdate'] = self.model.objects.filter(doctor=DoctorProfile.objects.get(user = self.request.user))
            context['doctors'] = DoctorProfile.objects.get(user = self.request.user)
        if status=='0':
            context['aptdate'] = context['aptdate'].filter(Q(status = status) & Q(date__gte=datetime.today()))
        elif status:
            context['aptdate'] = context['aptdate'].filter(Q(status = status))
        else:
            context['aptdate'] = context['aptdate'].filter(Q(date__gte=datetime.today()))
        return context


@login_required
def add_appointment(request):
    context = {}
    context['apttype'] = AppointmentTypes.objects.all()
    print(context['apttype'])
    print("ADD APPT")
    if request.method == 'GET':
        if is_user_patient(request.user):
            return HttpResponse("Unauthorized")
        form = appointmentForm()
        context["form"] = form
        context["fntype"] = "Create"
        return render(request, 'apt_create_view.html', context)
    elif request.method == 'POST':
        print("POST")
        doctor = DoctorProfile.objects.get(user = request.user)
        form = appointmentForm(request.POST)
        if form.is_valid():
            instance = form.save()
            instance.doctor = doctor
            instance.save()
            send_doctor_email(instance, request,'0')
            return HttpResponseRedirect('/appointments/?status=0&message=0')
        else:
            print(form.errors)
            context["form"] = form
            context["fntype"] = "Create"
            return render(request, 'apt_create_view.html', context)

@login_required
def edit_appointment(request,id):
    print("EDIT APPT")
    context = {}
    context['apttype'] = AppointmentTypes.objects.all()
    print(context['apttype'])
    if request.method == 'GET':
        appointment = get_object_or_404(Appointment, pk=id)
        if is_user_patient(request.user):
            if appointment.patient.user == request.user:
                form = patientAppointmentForm(instance=appointment)
            else:
                return HttpResponse("Unauthorized")
        else:
            form = appointmentForm(instance=appointment)
        context["form"] = form
        context["fntype"] = "Edit"
        return render(request, 'apt_create_view.html', context)
    elif request.method == 'POST':
        appointment = get_object_or_404(Appointment, pk=id)
        if is_user_patient(request.user):
            if appointment.patient.user == request.user:
                form = patientAppointmentForm(request.POST, instance=appointment)
            else:
                return HttpResponse("Unauthorized")
        else:
            form = appointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            #Send notification to user about changes
            send_doctor_email(appointment, request,'2')
            send_patient_email(appointment, request,'2')
            return HttpResponseRedirect('/appointments/?message=2&status='+str(appointment.status))
        else:
            print(form.errors)
            context["form"] = form
            context["fntype"] = "Edit"
            return render(request, 'apt_create_view.html', context)

def delete_appointment(request,id):
    appointment = get_object_or_404(Appointment, pk=id)
    if appointment.doctor.user == request.user:
        if(appointment.status != AppointmentStatus.OPEN):
            # Send notification to patient here
            notice = "Your appointment with Dr. " + appointment.doctor.user.get_full_name() + " at "+appointment.date.strftime('%d/%m/%Y')+", "+appointment.start_time.strftime("%H:%M")+" has been cancelled"
            print(notice)
            sendnoti(appointment.patient.user,
            {"head":"",
            "body":notice,
            "url":"/appointments/",
            }
            )
            appointment.status = AppointmentStatus.CANCELLED
            appointment.save()
            send_patient_email(appointment, request,'3')
            send_doctor_email(appointment, request,'3')
            return HttpResponseRedirect('/appointments/?message=3')
        appointment.delete()
        return redirect('appointments')
    else:
        return HttpResponse('You are not authorized to delete this appointment')

def cancel_appointment(request,id):
    if request.method == 'GET':
        appointment = get_object_or_404(Appointment, pk=id)
        if appointment.patient.user == request.user:
            if(appointment.status == AppointmentStatus.BOOKED):
                # Send notification to doctor here
                appointment.status = AppointmentStatus.CANCELLED
                appointment.save()
                Appointment.objects.create(doctor=appointment.doctor, date=appointment.date, start_time=appointment.start_time, end_time=appointment.end_time, status=AppointmentStatus.OPEN)
                send_doctor_email(appointment, request,'4')
                send_patient_email(appointment, request,'4')
                return HttpResponseRedirect('/appointments/?message=4&status=3')
            return HttpResponseRedirect('/appointments/')
        else:
            return HttpResponse('You are not authorized to cancel this appointment')

def complete_appointment(request,id):
    if request.method == 'GET':
        appointment = get_object_or_404(Appointment, pk=id)
        if appointment.patient.user == request.user:
            if(appointment.status == AppointmentStatus.CHECKED_IN):
                # Send notification to doctor here
                appointment.status = AppointmentStatus.COMPLETED
                appointment.save()
                send_patient_email(appointment, request,'6')
                send_doctor_email(appointment, request,'6')
                return HttpResponseRedirect('/appointments/?message=6&status=2')
            return HttpResponseRedirect('/appointments/')
        else:
            return HttpResponse('You are not authorized to checkin this appointment')

def cancelCheckIn_appointment(request,id):
    if request.method == 'GET':
        appointment = get_object_or_404(Appointment, pk=id)
        if appointment.patient.user == request.user:
            if(appointment.status == AppointmentStatus.CHECKED_IN):
                # Send notification to doctor here
                appointment.status = AppointmentStatus.BOOKED
                appointment.save()
                send_patient_email(appointment, request,'8')
                send_doctor_email(appointment, request,'8')
                return HttpResponseRedirect('/appointments/?message=8&status=1')
            return HttpResponseRedirect('/appointments/')
        else:
            return HttpResponse('You are not authorized to checkin this appointment')


def checkin_appointment(request,id):
    if request.method == 'GET':
        appointment = get_object_or_404(Appointment, pk=id)
        if appointment.patient.user == request.user:
            if(appointment.status == AppointmentStatus.BOOKED):
                # Send notification to doctor here
                appointment.status = AppointmentStatus.CHECKED_IN
                appointment.save()
                send_patient_email(appointment, request,'7')
                send_doctor_email(appointment, request,'7')
                return HttpResponseRedirect('/appointments/?message=7&status=4')
            return HttpResponseRedirect('/appointments/')
        else:
            return HttpResponse('You are not authorized to checkin this appointment')

def book_appointment(request,id):
    '''
    This function is called when a patient books or reschedules an appointment
    '''
    if is_user_patient(request.user):
        appointment = get_object_or_404(Appointment, pk=id)
        if(appointment.status == AppointmentStatus.OPEN):
            if request.POST.get('reschedule', None):
                print("RESCHEDULE")
                old_appointment = get_object_or_404(Appointment, pk=request.POST.get('reschedule', None))
                appointment.patient = old_appointment.patient
                appointment.status = AppointmentStatus.BOOKED
                appointment.apt_type = old_appointment.apt_type
                appointment.notes = old_appointment.notes
                appointment.save()
                if old_appointment.status == AppointmentStatus.BOOKED:
                    old_appointment.status = AppointmentStatus.OPEN
                old_appointment.save()
                send_patient_email(appointment, request,'5')
                send_doctor_email(appointment, request,'5')
                return HttpResponseRedirect('/appointments/?status=1&message=5')
            else:
                appointment.status = AppointmentStatus.BOOKED
                appointment.apt_type = request.POST.get('type', "")
                appointment.patient = PatientProfile.objects.get(user = request.user)
                appointment.save()
                send_patient_email(appointment, request,'1')
                send_doctor_email(appointment, request,'1')
                return HttpResponseRedirect('/appointments/?status=1&message=1')
        else:
            return HttpResponseRedirect('/appointments/?status=1&message=11')
    else:
        return HttpResponse('You are not authorized to book this appointment')

def bulk_apt_create(request):
    if request.method == 'GET':
        if is_user_patient(request.user):
            return HttpResponse("Unauthorized")
        context = {}
        return render(request, 'bulk_create.html',context)
    if request.method == 'POST':
        sdt = request.POST.get('sdt', '')
        sdt = list(map(int,sdt.split('-')))
        edt = request.POST.get('edt', '')
        edt = list(map(int,edt.split('-')))
        sdt = date(sdt[0], sdt[1], sdt[2])
        edt = date(edt[0], edt[1], edt[2])
        slot_names = request.POST.get('slot_name', None)
        slot_names = list(filter(None, slot_names.split(',')))
        print(slot_names)
        doctor = DoctorProfile.objects.get(user = request.user)
        for single_date in rrule(DAILY, dtstart=sdt, until=edt):
            print(single_date)
            for slot in slot_names:
                st = request.POST.get(f'st{slot}', None)
                et = request.POST.get(f'et{slot}',None)
                # print(st,et)
                st = datetime.strptime(st,'%H:%M')
                if et == '':
                    et = None
                else:
                    et = datetime.strptime(et,'%H:%M')
                appt = Appointment.objects.create(doctor=doctor, date=single_date, start_time=st, end_time=et, status=AppointmentStatus.OPEN)
                print(appt)
        return HttpResponseRedirect('/appointments/?status=0&message=0')

def send_noti(request):
    if request.method == 'GET':
        if is_user_patient(request.user):
            return HttpResponse("Unauthorized")
        context = {}
        return render(request, 'send_noti.html',context)
    if request.method == 'POST':
        date = request.POST.get('date')
        doctor = DoctorProfile.objects.get(user = request.user)
        appointments = Appointment.objects.filter(date=date,doctor=doctor,status=AppointmentStatus.BOOKED)
        for appointment in appointments:
            print(appointment)
            send_patient_email(appointment, request,'9')
        return HttpResponseRedirect('/appointments/?status=1&message=9')