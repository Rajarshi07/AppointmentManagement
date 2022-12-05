# Appointment Management

This is an appointment booking webapp made with django.

### Live Demo : [![Appointment Manager](./appointment_management/static/images/favicon.ico)Appointment Manager](https://AppointmentManager.rajarshi07.in)


## Technology Stack

1. HTML5
2. CSS3
3. JS
4. Django
5. Python 3.8


## Dependencies

- asgiref==3.4.1
- certifi==2021.10.8
- cffi==1.15.0
- charset-normalizer==2.0.7
- cryptography==35.0.0
- Django==3.2.8
- django-webpush==0.3.3
- http-ece==1.1.0
- idna==3.3
- py-vapid==1.8.2
- pycparser==2.20
- python-dateutil==2.8.2
- pytz==2021.3
- pywebpush==1.9.4
- requests==2.26.0
- six==1.16.0
- sqlparse==0.4.2
- urllib3==1.26.7

## Setup

**Run the following commands to get up and running**

1. `python3 -m pip install virtualenv`
2. `python3 -m virtualenv venv`

    

3. If OS is *Linux* or *macOS*,

    `source venv/bin/activate`

    If OS is *Windows*,

    `.\venv\Scripts\activate`

4. `cd appointment_management`
5. `python3 -m pip install -r requirements.txt`
6. `python3 manage.py collectstatic`
7. `python3 manage.py makemigrations`
8. `python3 manage.py migrate`
9. `python3 manage.py createsuperuser`
10. `python3 manage.py runserver`


## TEST ACCOUNTS

1. DOCTORS

        EMAIL: intricatetests1@gmail.com
        PASSWORD: qwertykey123

        EMAIL: intricatetests2@gmail.com
        PASSWORD: qwertykey123
2. PATIENTS

        EMAIL: intricatetesting1@gmail.com
        PASSWORD: qwertykey123

        EMAIL: intricatetesting2@gmail.com
        PASSWORD: qwertykey123

3. ADMIN (Not to be used for anything other than accessing admin panel. Modifying data from admin panel may lead to problems in the application.)

        EMAIL: appointmentmanagement
        PASSWORD: 1214

        EMAIL: admin
        PASSWORD: qwertykey123