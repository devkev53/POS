# Generated by Django 3.2.9 on 2021-11-18 20:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0023_auto_20211118_1523'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='storeinventory',
            name='entry',
        ),
        migrations.RemoveField(
            model_name='storeinventory',
            name='transfer',
        ),
    ]
