from django.contrib import admin
from .models import Product, Category
from import_export.admin import ImportExportModelAdmin

# Register your models here.


class CategoryAdmin (admin.ModelAdmin):
    list_display = ('name', 'description', 'userCreation', 'userUpdate')
    search_fields = ('name',)

class ProductAdmin (ImportExportModelAdmin):
   list_display = ('name', 'description', 'userCreation', 'userUpdate', 'price_in', 'price_out')
   search_fields = ('name',)
   list_filter = ('category','state')
   list_per_page = 10

   class Meta:
        model = Product



admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)

