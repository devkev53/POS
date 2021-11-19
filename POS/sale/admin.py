from django.contrib import admin
from .models import Sale, DetailSale, SaleBox
from employe.models import Employe
from django.contrib.auth.models import User

from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter

# Register your models here.

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