# Generated by Django 3.2.6 on 2021-10-01 18:59

import attendance.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0006_slackuser_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timesheet',
            name='date',
            field=models.DateField(default=attendance.models.getLocalTime),
        ),
    ]
