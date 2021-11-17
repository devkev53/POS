from django.db import models
from django.db.models.base import Model
from core.models import BaseModel, val_tel
from django.contrib.auth.models import User
from product.models import Product
from provider.models import Provider
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

# Create your models here.

class Store(BaseModel):
    name = models.CharField('Nombre', max_length=75)
    address = models.CharField('Direccion', max_length=125)
    phone = models.CharField(
        'Telefono', validators=[RegexValidator(
            regex=r'^[0-9]*$',
            message=('Ingrese solamente numeros'),
        ), val_tel], max_length=8, blank=True, null=True)
    # employe = models.ForeignKey(
    #     User, on_delete=models.CASCADE,
    #     verbose_name='Empleado', null=True, blank=True,)

    def __str__(self):
        return self.name

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Tienda'
        verbose_name_plural = 'Tiendas'

class StoreInventory(BaseModel):
    store = models.ForeignKey(
        Store, on_delete=models.CASCADE, verbose_name='Tienda')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name='Producto')
    stocks = models.PositiveIntegerField('Existencias', default=0)
    
    def __str__(self):
        return '%s, %s' % (self.product, self.stocks)

    class Meta:
        permissions = [('can_deliver_pizzas', 'Can deliver pizzas')]
        db_table = ''
        managed = True
        unique_together = ['store', 'product']
        verbose_name = 'Inventario en Tienda'
        verbose_name_plural = 'Inventario en Tiendas'

class BaseMove(BaseModel):
    comentary = models.TextField('Comentario')
    total = models.DecimalField('Subtotal', max_digits=12, decimal_places=2, editable=False, blank=True, null=True)


    def __str__(self):
        return '%s %s %s' % (self.origin, self.destiny, self.createDate)

    class Meta:
        abstract = True
        db_table = ''
        managed = True
        verbose_name = 'Movimiento'
        verbose_name_plural = 'Movimientos'

class BaseDetailMove(BaseModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name='Producto')
    quantity = models.PositiveSmallIntegerField('Cantidad')
    expiration = models.DateField(
        'Fecha de Expiracion', blank=True, null=True,
        help_text='Indispensable para productos perecederos')
    subtotal = models.DecimalField('Subtotal', max_digits=10, decimal_places=2, editable=False)

    def __str__(self):
        return (self.proproduct, self.quantity, self.subtotal)
    
    def calculate_subtotal(self):
        self.subtotal = self.product.price_in * self.quantity

    class Meta:
        abstract = True
        db_table = ''
        managed = True
        verbose_name = 'Detalle Movimiento'
        verbose_name_plural = 'Detalle Movimientos'

class Transfer(BaseMove):
    origin = models.ForeignKey(
        Store, on_delete=models.CASCADE, verbose_name='Origen',
        related_name='origin')
    destiny = models.ForeignKey(
        Store, on_delete=models.CASCADE, verbose_name='Destino',
        related_name='destiny')

    def __str__(self):
        return '%s %s %s' % (self.origin, self.destiny, self.createDate)
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Movimiento'
        verbose_name_plural = 'Movimientos'

    def calculate_total(self):
        for detail in DetailTransfer.objects.filter(Transfer=self.id):
            self.total += detail.subtotal 

    def clean(self) -> None:
        self.calculate_total()
        return super().clean()

class DetailTransfer(BaseDetailMove):
    tranfer = models.ForeignKey(
        Transfer, on_delete=models.CASCADE, verbose_name='Transferencia')

    def __str__(self):
        return (self.proproduct, self.quantity, self.subtotal)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Detalle Movimiento'
        verbose_name_plural = 'Detalle Movimientos'
    
    def check_origin_stock(self):
        if StoreInventory.objects.filter(id=self.tranfer.origin.id, product=self.product.id).exists():
            origin_quantity = StoreInventory.objects.filter(id=self.tranfer.origin.id, product=self.product.id).get()
            if self.quantity > origin_quantity.stocks:
                raise ValidationError(
                    'No hay suficientes existencias, únicamente hay: {}'.format(origin_quantity))
        else: 
            raise ValidationError(
                    'La tienda no cuenta con el producto')
    
    def add_destiny_stock(self):
        try:
            obj = StoreInventory.objects.get(id=self.tranfer.destiny.id, product=self.product.id)
            obj.stocks += self.quantity
            obj.save()
        except StoreInventory.DoesNotExist:
            obj = StoreInventory(store=self.destiny, product=self.product, stocks=self.quantity)
            obj.save()


    def clean(self) -> None:
        self.check_origin_stock()
        self.calculate_subtotal()
        self.add_destiny_stock()
        return super().clean()

class Entry(BaseMove):
    destiny = models.ForeignKey(
        Store, on_delete=models.CASCADE, verbose_name='Destino',
        related_name='sucursal')

    def __str__(self):
        return '%s, %s' % (self.destiny, self.total)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Entrada'
        verbose_name_plural = 'Entradas'
    
    def calculate_total(self):
        for detail in DetailEntry.objects.filter(entry=self.id):
            self.total += detail.subtotal 

    def clean(self) -> None:
        self.calculate_total()
        return super().clean()

class DetailEntry(BaseDetailMove):
    entry = models.ForeignKey(
        Entry, on_delete=models.CASCADE, verbose_name='Transferencia')
    provider = models.ForeignKey(
        Provider, on_delete=models.CASCADE, verbose_name='Proveedor')

    def __str__(self):
        return '%s, %s, %s' % (self.product, self.quantity, self.subtotal)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Detalle Entrada'
        verbose_name_plural = 'Detalle Entradas'

    def add_destiny_stock(self):
        try:
            obj = StoreInventory.objects.get(id=self.entry.destiny.id, product=self.product.id)
            obj.stocks += self.quantity
            obj.save()
        except StoreInventory.DoesNotExist:
            obj = StoreInventory(store=self.entry.destiny, product=self.product, stocks=self.quantity)
            obj.save()
        

    def clean(self) -> None:
        self.calculate_subtotal()
        self.add_destiny_stock()
        return super().clean()
