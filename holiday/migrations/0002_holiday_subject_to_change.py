# Generated by Django 3.2.6 on 2021-10-25 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('holiday', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='holiday',
            name='subject_to_change',
            field=models.BooleanField(default=False),
        ),
    ]