from django import forms
from .models import Appointment

# creating a form
class appointmentForm(forms.ModelForm):
    required_css_class = 'required'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    # create meta class
    class Meta:
        # specify model to be used
        model = Appointment
        # specify fields to be used
        fields = ["status","date","start_time","end_time","notes","patient","apt_type","billing_amount","payment_status"]



class patientAppointmentForm(forms.ModelForm):
    
    required_css_class = 'required'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    # create meta class
    class Meta:
        # specify model to be used
        model = Appointment
        # specify fields to be used
        fields = ["notes","apt_type"]
