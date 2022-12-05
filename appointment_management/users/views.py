from django.http.response import HttpResponseRedirect, JsonResponse, HttpResponse
from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import get_object_or_404, redirect,render
from django.contrib.auth.models import User,Group
from django.views.decorators.csrf import csrf_exempt
from webpush import send_user_notification,send_group_notification
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from appointments.models import Appointment
from users.models import *
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage
from users.tokens import account_activation_token
from users.utils import *
from django.contrib.auth.password_validation import validate_password,password_validators_help_text_html
from django.core.exceptions import ValidationError
from django.db import IntegrityError
# Create your views here.

@login_required
def profile(request):
    if request.method == 'GET':
        data={}
        if is_user_doctor(request.user):
            profile = DoctorProfile.objects.get(user=request.user)
            data['qualifications'] = profile.qualifications
            data['phone']=profile.phone
            return render(request,'profile.html',data)
        elif is_user_patient(request.user):
            profile = PatientProfile.objects.get(user=request.user)
            data['user']=request.user
            data['address']=profile.address
            data['dob']=profile.dob.strftime('%Y-%m-%d')
            data['phone']=profile.phone
            data['history']=profile.history
            print(data)
            return render(request,'profile.html',data)
        else:
            return redirect('/admin')
    elif request.method == 'POST':
        print(request.POST)
        try:
            if is_user_doctor(request.user):
                profile = DoctorProfile.objects.get(user=request.user)
                user = User.objects.get(username=request.user.username)
                user.first_name = request.POST.get('first_name')
                user.last_name = request.POST.get('last_name')
                user.email = request.POST.get('email')
                user.username = request.POST.get('email')
                profile.phone = request.POST.get('phone')
                profile.qualifications = request.POST.get('qualifications')
                user.save()
                profile.save()
                return HttpResponseRedirect('/?message=10')
            elif is_user_patient(request.user):
                profile = PatientProfile.objects.get(user=request.user)
                user = User.objects.get(username=request.user.username)
                user.first_name = request.POST.get('first_name')
                user.last_name = request.POST.get('last_name')
                user.email = request.POST.get('email')
                user.username = request.POST.get('email')
                profile.address = request.POST.get('address')
                profile.dob = request.POST.get('dob')
                profile.phone = request.POST.get('phone')
                profile.history = request.POST.get('history')
                user.save()
                profile.save()
                return HttpResponseRedirect('/?message=10')
        except IntegrityError:
            return HttpResponseRedirect('/users/profile?update=2')


def patient_profile(request,id):
    if request.method == 'GET':
        data={}
        if is_user_doctor(request.user):
            profile = PatientProfile.objects.get(id=id)
            data['patient'] = profile
            data['user']=profile.user
            data['address']=profile.address
            data['dob']=profile.dob.strftime('%Y-%m-%d')
            data['phone']=profile.phone
            data['history']=profile.history
            print(data)
            data['appointments'] = Appointment.objects.filter(patient=profile, doctor=DoctorProfile.objects.get(user = request.user))
            return render(request,'patient_profile.html',data)
        else:
            return redirect('/')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request,'login.html',{"msg":"Account activated successfully"})
    else:
        return HttpResponse('Activation link is invalid!')

def register(request):
    return render(request,'register.html',{"msg":""})

def doctor_register(request):
    if request.method == 'GET':
        return render(request,'register_dr.html',{"msg":password_validators_help_text_html()})
    elif request.method == 'POST':
        if request.POST.get('password') != request.POST.get('password_confirm'):
            return render(request,'register_dr.html',{"msg":"<ul><li>Passwords do not match</ul></li>"+password_validators_help_text_html()})
        try:
            validate_password(request.POST.get('password'))
            user = User.objects.create_user(username=request.POST.get('email'),first_name=request.POST.get('first_name'),last_name=request.POST.get('last_name'), password=request.POST.get('password'), email=request.POST.get('email'))
            user.is_active = False
            user.save()
        except ValidationError as e:
            a="<ul>"
            for i in e.messages:
                a+="<li>"+i+"</li>"
            a+="</ul>"
            print(a)
            return render(request,'register_dr.html',{"msg":a+password_validators_help_text_html()})
        except:
            return render(request,'register_dr.html',{"msg":"<ul><li>User already exists, Please try with another email.</ul></li>"+password_validators_help_text_html()})
        DoctorProfile.objects.create(user = user, qualifications = request.POST.get('qualifications'), phone = request.POST.get('phone'))
        current_site = get_current_site(request)
        mail_subject = 'Activate your Appointment Manager Account.'
        message = render_to_string('email_activation.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = request.POST.get('email')
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        return render(request,'register.html',{"msg":"You have been successfully registered. To activate your account please check your email."})

def patient_register(request):
    if request.method == 'GET':
        return render(request,'register_pt.html',{"msg":password_validators_help_text_html()})
    elif request.method == 'POST':
        if request.POST.get('password') != request.POST.get('password_confirm'):
            return render(request,'register_pt.html',{"msg":"<ul><li>Passwords do not match</ul></li>"+password_validators_help_text_html()})
        try:
            validate_password(request.POST.get('password'))
            user = User.objects.create_user(username=request.POST.get('email'),first_name=request.POST.get('first_name'),last_name=request.POST.get('last_name'), password=request.POST.get('password'), email=request.POST.get('email'))
            user.is_active = False
            user.save()
        except ValidationError as e:
            a="<ul>"
            for i in e.messages:
                a+="<li>"+i+"</li>"
            a+="</ul>"
            print(a)
            return render(request,'register_pt.html',{"msg":a+password_validators_help_text_html()})
        except:
            return render(request,'register_pt.html',{"msg":"<ul><li>User already exists, Please try with another email.</ul></li>"+password_validators_help_text_html()})
        PatientProfile.objects.create(user = user,address = request.POST.get('address'), phone = request.POST.get('phone'),dob = request.POST.get('dob'), history= request.POST.get('history'))
        current_site = get_current_site(request)
        mail_subject = 'Activate your Appointment Manager Account.'
        message = render_to_string('email_activation.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = request.POST.get('email')
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        return render(request,'register.html',{"msg":"You have been successfully registered. To activate your account please check your email."})

def loginpage(request):
    if(request.user.is_authenticated):
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('home')
            else:
                return render(request,'login.html',{"msg":"Account is not active"})
        else:
            try:
                user_temp = User.objects.get(username=username)
                if user_temp.is_active:
                    return render(request,'login.html',{"msg":"Invalid username/password"})
                else:
                    return render(request,'login.html',{"msg":"Account is not active. Check Email."})
            except:
                pass
            return render(request,'login.html',{"msg":"Invalid username/password"})
    return render(request,'login.html',{"msg":""})


def login_prev(request):
    return render(request,'login_prev.html',{"msg":""})

def logout_next(request):
    return render(request,'logout_next.html',{"msg":""})