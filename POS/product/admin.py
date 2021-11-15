from django.contrib import admin
from .models import Product, Category, DetailProduct

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    search_fields = ['name']

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(DetailProduct)