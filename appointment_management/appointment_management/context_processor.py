from django.conf import settings
from django.urls import reverse

def webpush_processor(request):
    vapid_public_key = getattr(settings, 'WEBPUSH_SETTINGS', {}).get('VAPID_PUBLIC_KEY', '')

    data = {'user': getattr(request, 'user', None),
            'vapid_public_key': vapid_public_key,
            'webpush_save_url': reverse('save_webpush_info')
            }
    return data

def user_processor(request):
    data = {'user': getattr(request, 'user', None)}
    data['is_doctor'] = False
    data['is_patient'] = False
    if data['user']:
        if request.user.is_authenticated:
                for group in request.user.groups.all():
                        if group.name == 'doctor':
                                data['is_doctor'] = True
                                data['is_patient'] = False
                                break
                        elif group.name == 'patient':
                                data['is_patient'] = True
                                data['is_doctor'] = False
                                break
    return data

def admin_header_processor(request):
    context = {}
    context['index_title'] =  "Welcome to Skin Studio"
    context['site_header'] = 'Skin Studio'
    context['site_name'] = 'Skin Studio'
    context['site_title'] = "Skin Studio - Admin Portal"
    return context