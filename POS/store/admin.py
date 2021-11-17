from django.contrib import admin
from django.db.models.query import QuerySet

from product.models import Product
from .models import Store, StoreInventory, Transfer, DetailTransfer, Entry, DetailEntry
from employe.models import Employe
from django.contrib.auth.models import User

# Register your models here.


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

    list_display = ('product', 'stocks','userCreation', 'userUpdate')
    list_filter = ('store', 'product__category')
    # inlines = [Inline,]
    # raw_id_fields = ('',)
    # readonly_fields = ('store',)
    search_fields = ('product',)
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
        elif request.user.groups.filter(
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


@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    '''Admin View for Transfer'''

    # list_display = ('',)
    # list_filter = ('',)
    inlines = [
        DetailTransferInline,
    ]
    # raw_id_fields = ('',)
    # readonly_fields = ('',)
    # search_fields = ('',)
    # date_hierarchy = ''
    # ordering = ('',)

    # Definimos que se muestren solo nuestra tienda
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        try:
            employe = Employe.objects.filter(user=request.user).get()
            if db_field.name == 'destiny':
                kwargs['queryset'] = Store.objects.filter(id=employe.store.id)
        except:
            pass
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class DetailEntryInline(admin.TabularInline):
    '''Tabular Inline View for DetailTransfer'''

    model = DetailEntry
    min_num = 1
    extra = 0
    autocomplete_fields = ('product', 'provider')


@admin.register(Entry)
class Entry(admin.ModelAdmin):
    '''Admin View for Transfer'''

    # list_display = ('',)
    # list_filter = ('',)
    inlines = [
        DetailEntryInline,
    ]
    # raw_id_fields = ('',)
    # readonly_fields = ('',)
    # search_fields = ('',)
    # date_hierarchy = ''
    # ordering = ('',)

    # Definimos que se muestren solo nuestra tienda
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        try:
            employe = Employe.objects.filter(user=request.user).get()
            if db_field.name == 'destiny':
                kwargs['queryset'] = Store.objects.filter(id=employe.store.id)
        except:
            pass
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(DetailEntry)