# Generated by Django 3.2.7 on 2021-09-30 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0006_alter_appointment_apt_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='apt_type',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
    ]