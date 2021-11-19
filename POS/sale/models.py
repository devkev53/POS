from django.db import models
from core.models import BaseModel
from store.models import StoreInventory, Store
from product.models import Product
from employe.models import Employe
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
# Create your models here.

STATEBOX_CHOICES = (
    (True, 'Caja Abierta'),
    (False, 'Caja Cerrada'),
)

class SaleBox(BaseModel):
    """Model definition for Box."""

    # TODO: Define fields here
    initial_mount = models.DecimalField(
        'Monto de Apertura', editable=False, max_digits=8, decimal_places=2, default=0.00)
    final_mount = models.DecimalField(
        'Monto de Apertura', editable=False, max_digits=8, decimal_places=2, default=0.00)
    state = models.BooleanField(
        'Estado de la Caja', help_text='Al crear la caja se apertura abierta por default',
        choices=STATEBOX_CHOICES, default=True)
    store = models.ForeignKey(
        Store, on_delete=models.CASCADE, editable=False, verbose_name='Tienda')

    class Meta:
        """Meta definition for Caja."""

        verbose_name = 'Caja'
        verbose_name_plural = 'Cajas'

    def __str__(self):
        """Unicode representation of MODELNAME."""
        return '%s, %s, %s' % (self.store, self.state, self.createDate)

    '''def clean(self):
        if SaleBox.objects.exists():
            last = SaleBox.objects.filter(store=self.store).last()
            if last.id != self.id:
                if last.state == True:
                    raise ValidationError(
                        'Existe una caja abierta')
        return super().clean()'''

    # TODO: Define custom methods here

    # Metodo para mostrar el monto inicial de la caja anterior
    def charge_initial_mount(self):
        if SaleBox.objects.filter(store=self.store).exists():
            last = SaleBox.objects.filter(store=self.store).last()
            self.initial_mount = last.final_mount
        else:
            self.initial_mount = 0.00


    # Metodo para cerrar la caja y dejar el monto final
    def close_box(self):
        return 0



class Sale(BaseModel):
    client = models.CharField('Cliente', max_length=75)
    nit = models.CharField('NIT', max_length=9, default='C/F')
    address = models.CharField('Direccion', max_length=75, default='Ciudad')
    total = models.DecimalField('Total', max_digits=8, decimal_places=2, default=0.00)
    salebox = models.ForeignKey(SaleBox, on_delete=models.CASCADE)

    def __str__(self):
        return '%s, %s, %s' % (self.createDate, self.client, self.total)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'

    def clean(self):
        if SaleBox.objects.exists(store=self.salebox.store):
            pass
        else:
            raise ValidationError(
                'La tienda no tiene una caja abiarta')
        return super().clean()


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