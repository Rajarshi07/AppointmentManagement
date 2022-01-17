
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from appointments.forms import appointmentForm,patientAppointmentForm
from appointments.models import Appointment
status_text_doctor = {
    '0':{
      'head':'Appointment Slot Created',
      'body':'New appointment slot has been added.',
    },
    '1':{
      'head':'Appointment Booked',
      'body':'Your appointment has been confirmed.',
    },
    '2':{
      'head':'Appointment Edited',
      'body':'Your appointment details have been edited.',
    },
    '3':{
      'head':'Appointment Deleted',
      'body':'This appointment slot has been cancelled. Please reschedule to another time.',
    },
    '4':{
      'head':'Appointment Cancelled',
      'body':'Thank you for contacting us, your appointment has been cancelled.',
    },
    '5':{
      'head':'Appointment Rescheduled',
      'body':'Your appointment has been rescheduled.',
    },
    '6':{
      'head':'Appointment Completed',
      'body':'Congratulations on completing your appointment. Please pay any fees dues(if any).',
    },
    '7':{
      'head':'Checked In',
      'body':'Congratulations,you have been checked in successfully.',
    },
    '8':{
      'head':'Cancelled Check In',
      'body':'Your appointment status is changed back to booked. Please check in when you reach the clinic.',
    },
  }
status_text_patient = {
    '0':{
      'head':'Appointment Slot Created',
      'body':'New appointment slot has been added.',
    },
    '1':{
      'head':'Appointment Booked',
      'body':'Your appointment has been confirmed.',
    },
    '2':{
      'head':'Appointment Edited',
      'body':'Your appointment details have been edited.',
    },
    '3':{
      'head':'Appointment Deleted',
      'body':'This appointment slot has been cancelled. Please reschedule to another time.',
    },
    '4':{
      'head':'Appointment Cancelled',
      'body':'Thank you for contacting us, your appointment has been cancelled.',
    },
    '5':{
      'head':'Appointment Rescheduled',
      'body':'Your appointment has been rescheduled.',
    },
    '6':{
      'head':'Appointment Completed',
      'body':'Congratulations on completing your appointment. Please pay any fees dues(if any).',
    },
    '7':{
      'head':'Checked In',
      'body':'Congratulations,you have been checked in successfully.',
    },
    '8':{
      'head':'Cancelled Check In',
      'body':'Your appointment status is changed back to booked. Please check in when you reach the clinic.',
    },
    '9':{
      'head':'Appointment Reminder',
      'body':'You have a booked appointment.',
    },
  }

def send_patient_email(appointment,request, status):
    try:
        print("sending email")
        current_site = get_current_site(request)
        mail_subject = status_text_patient[status]['head']
        message = render_to_string('email_apt_pt.html', {
            'appointment': appointment,
            'site': current_site,
            'form': appointmentForm(instance=appointment),
            'text': status_text_patient[status]['body'],
        })
        to_email = [appointment.patient.user.email]
        email = EmailMessage(
            mail_subject, message, to=to_email
        )
        email.content_subtype="html"
        email.send()
        print("sent")
    except Exception as e:
        print(e.message)

def send_doctor_email(appointment,request, status):
    try:
        current_site = get_current_site(request)
        mail_subject = status_text_doctor[status]['head']
        message = render_to_string('email_apt_dr.html', {
            'appointment': appointment,
            'site': current_site,
            'form': appointmentForm(instance=appointment),
            'text': status_text_doctor[status]['body'],
        })
        to_email = [appointment.doctor.user.email]
        email = EmailMessage(
            mail_subject, message, to=to_email
        )
        email.content_subtype="html"
        email.send()
    except Exception as e:
        print(e)
