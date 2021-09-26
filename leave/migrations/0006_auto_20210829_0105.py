# Generated by Django 3.2.6 on 2021-08-29 01:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0005_auto_20210829_0103'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.RemoveField(
            model_name='application',
            name='leave_type',
        ),
        migrations.AddField(
            model_name='application',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.RESTRICT, to='leave.category', verbose_name='Leave type'),
            preserve_default=False,
        ),
    ]
