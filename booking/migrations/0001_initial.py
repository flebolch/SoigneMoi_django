# Generated by Django 5.0.1 on 2024-01-30 04:24

import datetime
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DoctorProfile_temp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doctorFullName', models.CharField(max_length=100)),
                ('speciality', models.CharField(blank=True, max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Intervention_temp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('duration', models.PositiveSmallIntegerField()),
            ],
            options={
                'verbose_name': 'intervention',
                'verbose_name_plural': 'interventions',
            },
        ),
        migrations.CreateModel(
            name='PatientProfile_temp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patientFullName', models.CharField(max_length=100)),
                ('full_address', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Service_temp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'service',
                'verbose_name_plural': 'services',
            },
        ),
        migrations.CreateModel(
            name='Appointment_temp',
            fields=[
                ('appointment_id', models.AutoField(primary_key=True, serialize=False)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_start', models.DateTimeField()),
                ('date_stop', models.DateTimeField()),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.doctorprofile_temp')),
                ('intervention', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.intervention_temp')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.patientprofile_temp')),
            ],
            options={
                'verbose_name': 'appointment',
                'verbose_name_plural': 'appointments',
            },
        ),
        migrations.AddField(
            model_name='intervention_temp',
            name='service',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='booking.service_temp'),
        ),
        migrations.AddField(
            model_name='doctorprofile_temp',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.service_temp'),
        ),
        migrations.CreateModel(
            name='TimeSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slot_start', models.DateTimeField(default=datetime.time(0, 1))),
                ('slot_end', models.DateTimeField(default=datetime.time(23, 59))),
                ('is_available', models.BooleanField(default=True)),
                ('patient_available', models.IntegerField(default=5, validators=[django.core.validators.MinValueValidator(0)])),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.doctorprofile_temp')),
            ],
            options={
                'verbose_name': 'time_slot',
                'verbose_name_plural': 'time_slots',
            },
        ),
    ]
