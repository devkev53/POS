from django.db import models
from core.models import BaseModel
from store.models import StoreInventory
from product.models import Product

# Create your models here.


class Sale(BaseModel):
    client = models.CharField('Cliente', max_length=75)
    nit = models.CharField('NIT', max_length=9, default='C/F')
    address = models.CharField('Direccion', max_length=75, default='Ciudad')
    total = models.DecimalField('Total', max_digits=8, decimal_places=2, default=0.00)

    def __str__(self):
        return '%s, %s, %s' % (self.createDate, self.client, self.total)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'


class DetailSale(BaseModel):
    product = models.ForeignKey(
        StoreInventory, on_delete=models.CASCADE, verbose_name='Producto')
    quantity = models.PositiveIntegerField('Cantidad', default=0)
    subtotal = models.DecimalField('Subtotal', decimal_places=2, max_digits=7, default=0.00)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, verbose_name='Venta')
    
    def calculate_subtotal(self):
        subtotal_price_in = 0
        subtotal_price_out = 0
        product = Product.objects.filter(id=self.product.product.id).get()
        subtotal_price_in = float(product.price_in) * float(self.quantity)
        subtotal_price_out = float(product.price_out) * float(self.quantity)
        
        self.subtotal = subtotal_price_out

        return (subtotal_price_in, subtotal_price_out)
    
    def rest_to_stock(self):
        obj = StoreInventory.objects.filter(id=self.product.id).get()
        print(obj)
        obj.stocks -= self.quantity
        obj.save()

    def __str__(self):
        return '%s %s' % (self.product, self.subtotal)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalle de Ventas'
    
    def clean(self) -> None:
        return super().clean()
    
    def save(self):
        self.rest_to_stock()
        self.calculate_subtotal()
        super(DetailSale, self).save()