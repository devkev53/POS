# Generated by Django 3.2.9 on 2021-11-17 21:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_auto_20211117_2136'),
    ]

    operations = [
        migrations.RenameField(
            model_name='detailentry',
            old_name='tranfer',
            new_name='entry',
        ),
    ]
