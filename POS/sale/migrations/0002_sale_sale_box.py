# Generated by Django 3.2.9 on 2021-11-19 20:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='sale_box',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='sale.salebox'),
            preserve_default=False,
        ),
    ]
