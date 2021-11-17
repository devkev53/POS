from django.contrib import admin
from .models import Product, Category

# Register your models here.


class CategoryAdmin (admin.ModelAdmin):
    list_display = ('name', 'description', 'userCreation', 'userUpdate')
    search_fields = ('name',)
class ProductAdmin (admin.ModelAdmin):
   list_display = ('name', 'description', 'userCreation', 'userUpdate')
   search_fields = ('name',)
   list_filter = ('category','state')
   list_per_page = 10



admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)

