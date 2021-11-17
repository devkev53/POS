from django.db import models
from django.db.models.base import Model
from core.models import BaseModel

# Create your models here.


class Depot(BaseModel):
    name = models.CharField('Nombre', max_length=75)
    address = models.CharField('Direccion', max_length=125)
    phone = models.CharField('Telefono', max_length=8)

    def __str__(self):
        return self.name

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Bodega'
        verbose_name_plural = 'Bodegas'




