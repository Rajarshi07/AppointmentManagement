from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.conf.urls import url

urlpatterns =[
    # path('', views.appointments,name='appointments'),
    path('',views.AppointmentsList.as_view(),name='appointments'),
    path('add/', views.add_appointment,name='add_appointment'),
    path('add/multiple/',views.bulk_apt_create,name='multiple_appointments'),
    path('edit/<int:id>/', views.edit_appointment,name='edit_appointment'),
    path('delete/<int:id>/', views.delete_appointment,name='delete_appointment'),
    path('cancel/<int:id>/', views.cancel_appointment,name='cancel_appointment'),
    path('complete/<int:id>/', views.complete_appointment,name='complete_appointment'),
    path('checkin/<int:id>/', views.checkin_appointment,name='checkin_appointment'),
    path('checkout/<int:id>/', views.cancelCheckIn_appointment,name='cancelCheckIn_appointment'),
    path('book/<int:id>',views.book_appointment,name='book_appointment'),
    path('send_noti/',views.send_noti,name='send_notifications'),
]