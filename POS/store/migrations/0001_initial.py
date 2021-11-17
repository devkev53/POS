# Generated by Django 3.2.9 on 2021-11-17 16:37

import core.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0002_auto_20211117_1637'),
    ]

    operations = [
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createDate', models.DateField(auto_now=True, null=True, verbose_name='Fecha Modificacion:')),
                ('name', models.CharField(max_length=75, verbose_name='Nombre')),
                ('address', models.CharField(max_length=125, verbose_name='Direccion')),
                ('phone', models.CharField(blank=True, max_length=8, validators=[django.core.validators.RegexValidator(message='Ingrese solamente numeros', regex='^[0-9]*$'), core.models.val_tel], verbose_name='Telefono')),
                ('employe', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Empleado')),
                ('userCreation', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='Creadostore_store_related', to=settings.AUTH_USER_MODEL, verbose_name='Creado por:')),
                ('userUpdate', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='Modificadostore_store_related', to=settings.AUTH_USER_MODEL, verbose_name='Modificado por:')),
            ],
            options={
                'verbose_name': 'Tienda',
                'verbose_name_plural': 'Tiendas',
                'db_table': '',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='StoreInventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stocks', models.PositiveIntegerField(verbose_name='Existencias')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product', verbose_name='Producto')),
                ('store', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='store.store', verbose_name='Tienda')),
            ],
            options={
                'verbose_name': 'Inventario en Tienda',
                'verbose_name_plural': 'Inventario en Tiendas',
                'db_table': '',
                'managed': True,
            },
        ),
    ]
