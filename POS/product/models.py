from django.db import models
from django.db.models.fields import DateField
from core.models import BaseModel

# Create your models here.


STATE_CHOICES = (
    (0, 'Sin Existencias'),
    (1, 'Pocas Existencias'),
    (3, 'OK'),
)

class Category(BaseModel):
    name = models.CharField('Nombre', max_length=75)

    def __str__(self):
        return self.name

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

class Product(BaseModel):
    name = models.CharField('Nombre', max_length=100)
    description = models.TextField('Descripción', blank=True, null=True)
    state = models.PositiveSmallIntegerField('Estado', choices=STATE_CHOICES, default=0)
    category = models.ForeignKey(
        Category, verbose_name='Categoria', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'


class DetailProduct(BaseModel):
    """Model definition for DetailProduct."""

    # TODO: Define fields here
    lot = models.PositiveIntegerField('Lote', null=True)
    buy_price = models.FloatField('Precio de Compra')
    sale_price = models.FloatField('Precio de Venta')
    date_expiration = models.DateField('Fecha de Caducidad')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        """Meta definition for DetailProduct."""

        verbose_name = 'DetailProduct'
        verbose_name_plural = 'DetailProducts'

    def __str__(self):
        """Unicode representation of DetailProduct."""
        return self.product.name
