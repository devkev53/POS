# Generated by Django 3.2.9 on 2021-11-17 16:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'managed': True, 'verbose_name': 'Catalogo Categoria', 'verbose_name_plural': 'Catalogo Categorias'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'managed': True, 'verbose_name': 'Catalogo Producto', 'verbose_name_plural': 'Catalogo Productos'},
        ),
    ]
