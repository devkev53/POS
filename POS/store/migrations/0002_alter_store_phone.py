# Generated by Django 3.2.9 on 2021-11-17 16:38

import core.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='phone',
            field=models.CharField(blank=True, max_length=8, null=True, validators=[django.core.validators.RegexValidator(message='Ingrese solamente numeros', regex='^[0-9]*$'), core.models.val_tel], verbose_name='Telefono'),
        ),
    ]
