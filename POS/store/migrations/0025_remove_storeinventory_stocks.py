# Generated by Django 3.2.9 on 2021-11-18 20:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0024_auto_20211118_2005'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='storeinventory',
            name='stocks',
        ),
    ]
