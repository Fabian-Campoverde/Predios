# Generated by Django 4.2.5 on 2023-10-03 16:10

from django.db import migrations, models
import erp.userauths.models


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0006_alter_profile_dni'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='DNI',
            field=models.PositiveIntegerField(validators=[erp.userauths.models.validate_dni_length]),
        ),
    ]
