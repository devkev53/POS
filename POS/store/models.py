from django.db import models
from core.models import BaseModel

# Create your models here.


class Store(models.Model):
    """Model definition for Sale."""
    name = models.CharField('Nombre', max_length=150)
    address = models.CharField('Direccion', max_length=100)
    phone = models.CharField('Telefono', max_length=8)

    # TODO: Define fields here

    class Meta:
        """Meta definition for Sale."""

        verbose_name = 'Tienda'
        verbose_name_plural = 'Tiendas'

    def __str__(self):
        """Unicode representation of Sale."""
        return self.name