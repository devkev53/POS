from django.contrib import admin
from .models import Provider

# Register your models here.

@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    '''Admin View for Provider'''

    list_display = ('name', 'address', 'phone')
    # list_filter = ('',)
    # inlines = [Inline,]
    # raw_id_fields = ('',)
    # readonly_fields = ('',)
    search_fields = ('name',)
    # date_hierarchy = ''
    # ordering = ('',)
