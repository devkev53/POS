from django.db import models
from core.models import BaseModel
from store.models import StoreInventory, Store
from product.models import Product
from employe.models import Employe

# Create your models here.

STATEBOX_CHOICES = (
    (True, 'Caja Abierta'),
    (False, 'Caja Cerrada'),
)

class SaleBox(BaseModel):
    """Model definition for Box."""

    # TODO: Define fields here
    initial_mount = models.DecimalField(
        'Monto de Apertura', editable=False, max_digits=8, decimal_places=2)
    final_mount = models.DecimalField(
        'Monto de Apertura', editable=False, max_digits=8, decimal_places=2)
    state = models.BooleanField(
        'Estado de la Caja', help_text='Al crear la caja se apertura abierta por default',
        choices=STATEBOX_CHOICES, default=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, editable=False)

    class Meta:
        """Meta definition for Caja."""

        unique_together = []
        verbose_name = 'Caja'
        verbose_name_plural = 'Cajas'

    def __str__(self):
        """Unicode representation of MODELNAME."""
        pass

    def save(self):
        super(DetailSale, self).save()

    # TODO: Define custom methods here

    # Metodo para mostrar el monto inicial de la caja anterior
    def charge_initial_mount(self):
        return 0


    # Metodo para cerrar la caja y dejar el monto final
    def close_box(self):
        return 0



class Sale(BaseModel):
    Store = models.ForeignKey(Store, on_delete=models.CASCADE)
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