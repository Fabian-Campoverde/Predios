# Generated by Django 4.2.5 on 2023-10-08 14:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0011_predio_deuda_construccion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='phone',
        ),
    ]
