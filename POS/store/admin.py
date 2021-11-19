from django.contrib import admin
from django.contrib.admin.decorators import action
from django.db.models.query import QuerySet

from product.models import Product
from .models import Store, StoreInventory, Transfer, DetailTransfer, Entry, DetailEntry
from employe.models import Employe
from django.contrib.auth.models import User

from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter

# Register your models here.

# Metodo que cambia el estado de las Entradas o Movimientos
def change_state(self, val, request, queryset):
    if request.user.groups.filter(
            name='Gerente').exists() or request.user.groups.filter(
            name='Administrador').exists():
            for row in queryset.filter(state=0):
                self.log_change(request, row, 'Aprobar')
            rows_update = 0

            for obj in queryset:
                if not obj.state:
                    obj.state = val
                    obj.save()

                    rows_update += 1
            if rows_update == 1:
                message_bit = 'Ingreso Aprobado'
            else:
                message_bit = '%s Ingresos Aprobados' % rows_update
                self.message_user(request, '%s satisfactoriamente como aprobados' % message_bit)

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    '''Admin View for Store'''

    list_display = ('name','address','phone', 'userCreation', 'userUpdate')
    # list_filter = ('',)
    # inlines = ['',]
    # raw_id_fields = ('',)
    # readonly_fields = ('',)
    search_fields = ('name','addess')
    # date_hierarchy = ''
    # ordering = ('',)

@admin.register(StoreInventory)
class StoreInventoryAdmin(admin.ModelAdmin):
    '''Admin View for StoreInventory'''

    list_display = ('product', 'stocks','userCreation')
    list_filter = ('store', 'product__category')
    # inlines = [Inline,]
    # raw_id_fields = ('',)
    # readonly_fields = ('store',)
    search_fields = ('product__name',)
    autocomplete_fields = ('product',)
    # date_hierarchy = ''
    # ordering = ('',)

    # Definimos que se muestren solo nuestra tienda
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        try:
            employe = Employe.objects.filter(user=request.user).get()
            if db_field.name == 'store':
                kwargs['queryset'] = Store.objects.filter(id=employe.store.id)
        except:
            pass
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


    # Definimos que el listado se muestre solo a los empleados
    def get_queryset(self, request, *args, **kwargs):
        qs = super(StoreInventoryAdmin, self).get_queryset(
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
            return None

    # Guardamos automaticamnte la tienda del empleado
    '''def save_mode(self, request, obj, form, change):
        try:
            employe = Employe.objects.filter(user=request.user).get()
            obj.store = employe.store
        except:
            pass
        super().save_model(request, obj, form, change)'''

class DetailTransferInline(admin.TabularInline):
    '''Tabular Inline View for DetailTransfer'''

    model = DetailTransfer
    min_num = 1
    extra = 0
    autocomplete_fields = ('product',)
    readonly_fields = ('subtotal',)

@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    '''Admin View for Transfer'''

    list_display = ('createDate','origin', 'destiny', 'calculate_total', 'userCreation', 'state_transfer')
    list_filter = (
        ('createDate', DateRangeFilter),
        'state')
    inlines = [
        DetailTransferInline,
    ]
    # raw_id_fields = ('',)
    # readonly_fields = (,)
    search_fields = ('userCreation', 'createDate', 'origin', 'destiny')
    # date_hierarchy = ''
    actions = ['approve_entry', 'reject_entry',]

    # Definimos que el listado se muestre solo a los empleados
    def get_queryset(self, request, *args, **kwargs):
        qs = super(TransferAdmin, self).get_queryset(
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
            qs_store = qs.filter(destiny=employe.store.id) | qs.filter(origin=employe.store.id)
            return qs_store
        else:
            return None

    # Definimos que se muestren solo nuestra tienda
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        try:
            employe = Employe.objects.filter(user=request.user).get()
            if db_field.name == 'destiny':
                kwargs['queryset'] = Store.objects.filter(id=employe.store.id)
        except:
            pass
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # Funcion para mostrar el rango de fechas en el filtro
    def get_rangefilter_created_at_title(self, request, field_path):
        return 'custom title'

    # Funcion para Arpobar las entradas
    def approve_entry(self, request, queryset, *args, **kwargs):
        change_state(self, 1, request, queryset)
        for row in queryset.filter(state=1):
            for d in DetailTransfer.objects.filter(transfer=row):
                d.add_destiny_stock()
    approve_entry.short_description = 'Aprobar Movimientos'

    # Funcion para Rechazar las entradas
    def reject_entry(self, request, queryset, *args, **kwargs):
        change_state(self, 2, request, queryset)
    reject_entry.short_description = 'Rechazar Movimientos'

class DetailEntryInline(admin.TabularInline):
    '''Tabular Inline View for DetailTransfer'''

    model = DetailEntry
    min_num = 1
    extra = 0
    autocomplete_fields = ('product', 'provider')
    readonly_fields = ('subtotal',)

@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    '''Admin View for Transfer'''

    list_display = ('createDate', 'destiny', 'calculate_total', 'userCreation', 'state_entry')
    list_filter = (
        ('createDate', DateRangeFilter),
        'state')
    inlines = [
        DetailEntryInline,
    ]
    # raw_id_fields = ('',)
    # readonly_fields = ('',)
    search_fields = ('userCreation', 'createDate')
    # date_hierarchy = ''
    # ordering = ('',)
    actions = ['approve_entry', 'reject_entry',]

    # Definimos que el listado se muestre solo a los empleados
    def get_queryset(self, request, *args, **kwargs):
        qs = super(EntryAdmin, self).get_queryset(
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
            qs_store = qs.filter(destiny=employe.store.id)
            return qs_store
        else:
            return None

    # Definimos que se muestren solo nuestra tienda
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        try:
            employe = Employe.objects.filter(user=request.user).get()
            if db_field.name == 'destiny':
                kwargs['queryset'] = Store.objects.filter(id=employe.store.id)
        except:
            pass
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # Funcion para mostrar el rango de fechas en el filtro
    def get_rangefilter_created_at_title(self, request, field_path):
        return 'custom title'

    # Funcion para Arpobar las entradas
    def approve_entry(self, request, queryset, *args, **kwargs):
        change_state(self, 1, request, queryset)
        for row in queryset.filter(state=1):
            for d in DetailEntry.objects.filter(entry=row):
                d.add_destiny_stock()
    approve_entry.short_description = 'Aprobar Entradas'

    # Funcion para Rechazar las entradas
    def reject_entry(self, request, queryset, *args, **kwargs):
        change_state(self, 2, request, queryset)
    reject_entry.short_description = 'Rechazar Entradas'



