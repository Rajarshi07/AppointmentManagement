"""appointment_management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
import appointment_management.views as views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.views.generic import TemplateView, RedirectView
from django.contrib.auth.views import LogoutView

admin.site.site_header = "Appointment Manager"
admin.site.site_title = "Appointment Manager - Admin Portal"
admin.site.index_title = "Welcome to Appointment Manager"
admin.site.login_template = "login.html"
auth_views.PasswordResetView.template_name = 'password_reset_form.html'
auth_views.PasswordResetView.email_template_name = 'password_reset_email.html'
auth_views.PasswordResetDoneView.template_name = 'password_reset_done.html'
auth_views.PasswordResetConfirmView.template_name = 'password_reset_confirm.html'
auth_views.PasswordResetCompleteView.template_name = 'password_reset_complete.html'
auth_views.PasswordChangeView.template_name = 'password_change_form.html'
auth_views.PasswordChangeDoneView.template_name = 'password_change_done.html'
urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls,name='admin'),
    path('users/', include('users.urls')),
    path('', views.home,name='home'),
    path('appointments/', include('appointments.urls')),
    path('webpush/', include('webpush.urls')),
    path('sw.js', TemplateView.as_view(template_name='sw.js', content_type='application/x-javascript')),
    url(r'^favicon\.ico$',RedirectView.as_view(url='/static/images/favicon.ico')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
