# Generated by Django 5.0.1 on 2024-02-18 07:50

import django.db.models.deletion
import planningmanager.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planningmanager', '0002_service_doctorprofile_service'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slot_start', models.DateTimeField(default=planningmanager.models.TimeSlot.get_default_start_time)),
                ('slot_end', models.DateTimeField(blank=True, null=True)),
                ('is_available', models.BooleanField(default=True)),
                ('patient_available', models.IntegerField(default=5)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='planningmanager.doctorprofile')),
            ],
            options={
                'verbose_name': 'time_slot',
                'verbose_name_plural': 'time_slots',
            },
        ),
    ]