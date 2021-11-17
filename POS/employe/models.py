from django.db import models
from django.contrib.auth.models import User
from store.models import Store
from core.models import BaseModel, val_tel
from django.core.validators import RegexValidator


# Create your models here.
ROLE_CHOICES = (
    (0, 'Gerente'),
    (1, 'Administrador'),
    (2, 'Vendedor'),
)


class Employe(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(
        'Telefono', validators=[RegexValidator(
            regex=r'^[0-9]*$',
            message=('Ingrese solamente numeros'),
        ), val_tel], max_length=8, blank=True, null=True)
    role = models.PositiveSmallIntegerField('Rol', choices=ROLE_CHOICES, default=0)
    store = models.ForeignKey(
        Store, on_delete=models.CASCADE, verbose_name='Tienda',
        blank=True, null=True)

    def __str__(self):
        name = ''
        if self.user.first_name:
            name = self.user.first_name + ' ' + self.user.last_name
        else: 
            name = self.user.username
        return name

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'
