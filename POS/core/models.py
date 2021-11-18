from django.db import models
from django.contrib.auth.models import User
from crum import get_current_user # Utilizamos para realizar la auditoria
from django.core.exceptions import ValidationError

# Create your models here.

# Metodo que valida el Numero de Telefono
def val_tel(value):
    ''' Metodo que valida el numero de telefono y solo permite
    numeros, ademas no permite cadenas mayores a ocho numeros '''
    if len(value) > 8 or len(value) < 7:  # Si el largo es menor de 7
        raise ValidationError(  # Muesra un mensaje de error
            'Ingrese un numero de telefono valido')

# Se usara este modelo como base para generar una auditoria de creacion y actualizacion
class BaseModel(models.Model):
    userCreation = models.ForeignKey(
        User, on_delete=models.PROTECT, blank=True, null=True,
        verbose_name='Creado por:', related_name='Creado%(app_label)s_%(class)s_related',
        editable=False)
    createDate = models.DateField('Fecha Creacion:', auto_now_add=True, blank=True, null=True)
    userUpdate = models.ForeignKey(
        User, on_delete=models.PROTECT, blank=True, null=True,
        verbose_name='Modificado por:', related_name='Modificado%(app_label)s_%(class)s_related',
        editable=False)
    updateDate = models.DateField('Fecha Modificacion:', auto_now=True, blank=True, null=True)

    class Meta:
        abstract = True
        verbose_name = 'BaseModel'
        verbose_name_plural = 'BaseModels'

    def save(self):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.userCreation = user
            else:
                self.userUpdate = user
        super(BaseModel, self).save()
