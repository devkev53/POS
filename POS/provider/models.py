from django.db import models
from core.models import BaseModel, val_tel
from django.core.validators import RegexValidator


# Create your models here.


class Provider(models.Model):
    name = models.CharField('Nombre', max_length=75)
    address = models.CharField('Direccion', max_length=125)
    phone = models.CharField(
        'Telefono', validators=[RegexValidator(
            regex=r'^[0-9]*$',
            message=('Ingrese solamente numeros'),
        ), val_tel], max_length=8, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'