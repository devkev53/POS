from django.db import models
from product.models import Product
from store.models import Store
from core.models import BaseModel
from POS.settings import AUTH_USER_MODEL
from crum import get_current_user # Utilizamos para realizar la auditoria


# Create your models here.


STATE_MOVE_CHOICES = (
    (0, 'Pendiente'),
    (1, 'Aprobado'),
    (3, 'Rechazado'),
)

class Move(BaseModel):
    """Model definition for Movimiento."""

    # TODO: Define fields here
    origin = models.ForeignKey(
        Store, on_delete=models.CASCADE, related_name='Origin',
        verbose_name='Origen') 
    destiny = models.ForeignKey(
        Store, on_delete=models.CASCADE, related_query_name='destiny',
        verbose_name='Destino')
    state = models.PositiveSmallIntegerField(
        'Estado', choices=STATE_MOVE_CHOICES, default=0)
    requested = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='requested', verbose_name='Solicitado por',
        editable=False, null=True, blank=True)
    checked = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='cheked', verbose_name='Autorizado/Rechazado por',
        editable=False, null=True, blank=True)


    class Meta:
        """Meta definition for Movimiento."""

        verbose_name = 'Movimiento'
        verbose_name_plural = 'Movimientos'

    def __str__(self):
        """Unicode representation of Movimiento."""
        return  '%s, %s' % (self.createDate, self.origin)

    def save(self):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.requested = user
                self.userCreate = user
            else:
                self.userUpdate = user
                if self.state != 0:
                    self.checked = user

        super(Move, self).save()



class DetailMove(BaseModel):
    """Model definition for DetalleMovimiento."""

    # TODO: Define fields here
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name='Producto')
    quantity = models.PositiveIntegerField('Cantidad')
    move = models.ForeignKey(Move, on_delete=models.CASCADE, verbose_name='Movimiento')
    lot = models.CharField('Lote', max_length=50)
    subtotal = models.FloatField('Subtotal')

    class Meta:
        """Meta definition for DetalleMovimiento."""

        verbose_name = 'Detalle de Movimiento'
        verbose_name_plural = 'Detalle de Movimientos'

    def __str__(self):
        """Unicode representation of DetalleMovimiento."""
        pass


