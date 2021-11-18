from django.db import models
from core.models import BaseModel

# Create your models here.



class Category(BaseModel):
    name = models.CharField('Nombre', max_length=75)
    description = models.TextField('Descripción', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Catalogo Categoria'
        verbose_name_plural = 'Catalogo Categorias'


class Product(BaseModel):
    name = models.CharField('Nombre', max_length=75)
    description = models.TextField('Descripción', blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name='Categoria', 
        blank=True, null=True)
    state = models.BooleanField('Estado', default=False)
    price_in = models.DecimalField('Precio Compra', max_digits=8, decimal_places=2, default=0)
    price_out = models.DecimalField('Precio Venta', max_digits=8, decimal_places=2, default=0)



    def __str__(self):
        return self.name

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Catalogo Producto'
        verbose_name_plural = 'Catalogo Productos'