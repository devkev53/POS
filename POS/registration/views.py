from django.contrib.auth.base_user import AbstractBaseUser
from django.forms import fields
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from .models import User
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from .models import Profile

from .forms import UserCreationFormWithEmail, EmailForm, ProfileForm

from django.db import transaction
# Importamos los decoradores
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

# PDB
import pdb

# Create your views here.

# Crear Usuario

class ProfileCreate(CreateView):
    model = Profile
    form_class = ProfileForm
    success_url = reverse_lazy('users-list')
    url_redirect = success_url
    template_name = 'registration/user_form.html'

    # @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            # prod = Producto.objects.filter(id=request.POST['id']).get()
            if action == 'add':
                with transaction.atomic():
                    # Creamos el Usuario
                    requestPedido = json.loads(request.POST['ingr'])
                    nuevoPedido = Pedido()
                    nuevoPedido.fecha = requestPedido['fecha']
                    nuevoPedido.referencia = requestPedido['referencia']
                    nuevoPedido.totalConsultora = float(requestPedido['totalConsultora'])
                    nuevoPedido.totalCatalogo = float(requestPedido['totalCatalogo'])
                    nuevoPedido.save()

                    # Creamos el perfil
                    for i in requestPedido['productos']:
                        det = DetallePedido()
                        det.pedido = nuevoPedido
                        det.producto = Producto.objects.filter(id=i['id']).get()
                        det.pConsultora = float(i['precio_consultora'])
                        det.pCatalogo = float(i['precio_catalogo'])
                        det.cantidad = int(i['cantidad'])
                        det.save()
            else:
                data['error'] = 'No ha ingresado a Ninguna Opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'add'
        context['titulo'] = 'Registrar Pedido'
        context['lazyUrl'] = self.url_redirect
        context['contentAlert'] = 'Esta seguro de registrar este pedido..!'
        context['titleAlert'] = 'Registrar nuevo Pedido'
        context['formUser'] = UserCreationFormWithEmail 
        return context

class UserCreateView(CreateView):
    model = User
    form_class = UserCreationFormWithEmail
    success_url = reverse_lazy('users-list')

    


# Listado de Usuarios
class UserListView(ListView):

    model = User
    template_name = 'registration/list_user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context