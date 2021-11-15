from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.db.models.base import Model
from django.db.models.fields.related import OneToOneField # Modificaremos el usuario de django
from POS.settings import AUTH_USER_MODEL # Importamos el model de usuario a usar
from core.models import BaseModel # Importamos el modelo que servira como base

# Create your models here.


# Create your models here.
ROLE_CHOICES = [
    ('0', 'Gerente'),
    ('1', 'Administrador'),
    ('2', 'Vendedor'),
]

GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
]

class User(AbstractUser):
    userCreation = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True,
        verbose_name='Creado por:', related_name='Creado%(app_label)s_%(class)s_related')
    createDate = models.DateField('Fecha Creacion:', auto_now_add=True, blank=True, null=True)
    userUpdate = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True,
        verbose_name='Modificado por:', related_name='Modificado%(app_label)s_%(class)s_related')
    createDate = models.DateField('Fecha Modificacion:', auto_now=True, blank=True, null=True)
    role = models.PositiveSmallIntegerField('Rol', choices=ROLE_CHOICES, default=2, blank=True, null=True)
    cui = models.CharField('CUI', max_length=15)
    phone = models.CharField('Telefono', max_length=8)
    gender = models.CharField('Genero', choices=GENDER_CHOICES, default='M', max_length=1)
