# Generated by Django 3.2.6 on 2021-10-21 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0009_auto_20211012_1559'),
    ]

    operations = [
        migrations.AddField(
            model_name='shift',
            name='buffer_time',
            field=models.PositiveIntegerField(default=15, help_text='Buffer time in minutes'),
        ),
        migrations.AddField(
            model_name='shift',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='shift',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='shift',
            unique_together={('from_time', 'to_time', 'buffer_time')},
        ),
    ]
