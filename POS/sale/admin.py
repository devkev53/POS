from django.contrib import admin
from .models import Sale, DetailSale, SaleBox
from store.models import Store
from employe.models import Employe
from django.contrib.auth.models import User
from import_export.admin import ImportExportModelAdmin


from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter

# Register your models here.

# Funcion para mostrar unicamente el QuerySet de la tienda asingada al usuario
def set_queryset_employe(request):
        try:
            employe = Employe.objects.filter(user=request.user).get()
        except:
            pass
        if request.user.is_superuser:
            return qs
        if request.user.groups.filter(
            name='Gerente').exists() or request.user.groups.filter(
                name='Administrador').exists():
            qs_store = qs.filter(store=employe.store.id)
            return qs_store
        else:
            return None


class DetailSaleInline(admin.TabularInline):
    '''Tabular Inline View for DetailSale'''

    model = DetailSale
    min_num = 1
    extra = 0
    autocomplete_fields = ('product',)
    readonly_fields = ('subtotal',)

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    '''Admin View for Sale'''

    list_display = ('createDate', 'userCreation', 'client', 'total')
    list_filter = (
        ('createDate', DateRangeFilter),
        )
    inlines = [
        DetailSaleInline,
    ]
    # raw_id_fields = ('',)
    readonly_fields = ('total',)
    search_fields = ('userCreation', 'createDate', 'client')
    # date_hierarchy = ''
    # ordering = ('',)

    # Funcion para mostrar el rango de fechas en el filtro
    def get_rangefilter_created_at_title(self, request, field_path):
        return 'custom title'


@admin.register(SaleBox)
class SaleBoxAdmin(admin.ModelAdmin):
    '''Admin View for '''

    # list_display = ('',)
    # list_filter = ('',)
    # inlines = [
    #     Inline,
    # ]
    # raw_id_fields = ('',)
    readonly_fields = ('store', 'createDate', 'state')
    # search_fields = ('',)
    # date_hierarchy = ''
    # ordering = ('',)
    actions = ['cloxe_box',]

    # Metodo Para Cerra Caja
    def close_box(self, request, queryset):
        for row in queryset.filter(state=True):
            self.log_change(request, row, 'Cerrar Caja')
        rows_update = 0

        for obj in queryset:
            if not obj.state:
                obj.state = False
                obj.save()

                rows_update += 1
        if rows_update == 1:
            message_bit = 'Caja Cerrada'
        else:
            message_bit = '%s Cajas Cerradas' % rows_update
            self.message_user(request, '%s satisfactoriamente como cerradas' % message_bit)
    close_box.short_description = 'Cerrar Caja'

    def save_model(self, request, obj, form, change):
        empleado = Employe.objects.filter(user=request.user).get()
        empleado_store = Store.objects.filter(id=empleado.store.id).get()
        obj .store = empleado_store
        super().save_model(request, obj, form, change)

    '''def get_queryset(self, request, *args, **kwargs):
        qs = super(SaleBoxAdmin, self).get_queryset(
            request, *args, **kwargs)
        try:
            employe = Employe.objects.filter(user=request.user).get()
        except:
            pass
        if request.user.is_superuser:
            return qs
        if request.user.groups.filter(
            name='Gerente').exists() or request.user.groups.filter(
                name='Administrador').exists():
            qs_store = qs.filter(store=employe.store.id)
            return qs_store
        else:
            return None'''

    
