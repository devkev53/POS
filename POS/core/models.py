from django.db import models
from POS.settings import AUTH_USER_MODEL # Importamos el model de usuario a usar
from crum import get_current_user # Utilizamos para realizar la auditoria


# Create your models here.

class BaseModel(models.Model):
    userCreation = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True,
        verbose_name='Creado por:', related_name='Creado%(app_label)s_%(class)s_related',
        editable=False)
    createDate = models.DateField('Fecha Creacion:', auto_now_add=True, blank=True, null=True)
    userUpdate = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True,
        verbose_name='Modificado por:', related_name='Modificado%(app_label)s_%(class)s_related',
        editable=False)
    createDate = models.DateField('Fecha Modificacion:', auto_now=True, blank=True, null=True)

    class Meta:
        abstract = True
        verbose_name = 'BaseModel'
        verbose_name_plural = 'BaseModels'

    def save(self):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.userCreate = user
            else:
                self.userUpdate = user
        super(BaseModel, self).save()