# Generated by Django 3.2.9 on 2021-11-17 19:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_detailtransfer_transfer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='detailtransfer',
            old_name='trasnfer',
            new_name='tranfer',
        ),
    ]
