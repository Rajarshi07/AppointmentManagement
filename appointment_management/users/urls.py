from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.conf.urls import url

urlpatterns =[
    path('loginprev/', views.login_prev,name='loginprev'),
    path('login/', views.loginpage,name='login'),
    path('register/', views.register,name='register'),
    path('register/doctor', views.doctor_register,name='doctor_register'),
    path('register/patient', views.patient_register,name='patient_register'),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
    path('profile/', views.profile,name='profile'),
    path('patient_profile/<int:id>/',views.patient_profile,name='patient_profile'),
    path('logout', LogoutView.as_view(next_page='loggedout'), name='logout'),
    path('loggedout', views.logout_next, name='loggedout'),
]