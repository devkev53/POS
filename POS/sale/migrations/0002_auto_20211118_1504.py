# Generated by Django 3.2.9 on 2021-11-18 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='detailsale',
            name='updateDate',
            field=models.DateField(auto_now=True, null=True, verbose_name='Fecha Modificacion:'),
        ),
        migrations.AddField(
            model_name='sale',
            name='updateDate',
            field=models.DateField(auto_now=True, null=True, verbose_name='Fecha Modificacion:'),
        ),
        migrations.AlterField(
            model_name='detailsale',
            name='createDate',
            field=models.DateField(auto_now_add=True, null=True, verbose_name='Fecha Creacion:'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='createDate',
            field=models.DateField(auto_now_add=True, null=True, verbose_name='Fecha Creacion:'),
        ),
    ]
