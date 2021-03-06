# Generated by Django 3.2.6 on 2021-10-12 09:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('attendance', '0008_auto_20211003_1935'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shift',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('from_time', models.TimeField(verbose_name='From')),
                ('to_time', models.TimeField(verbose_name='To')),
            ],
        ),
        migrations.AlterModelOptions(
            name='checkin',
            options={'ordering': ['time']},
        ),
        migrations.AlterModelOptions(
            name='checkout',
            options={'ordering': ['time']},
        ),
        migrations.AlterModelOptions(
            name='timesheet',
            options={'ordering': ['-date']},
        ),
        migrations.AddField(
            model_name='timesheet',
            name='is_late',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='ShiftUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shift', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='users', to='attendance.shift')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='shift', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'shift')},
            },
        ),
    ]
