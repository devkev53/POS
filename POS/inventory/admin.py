from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from .models import Move, DetailMove

# Register your models here.


class DetailMoveInline(admin.TabularInline):
    model = DetailMove
    extra = 0
    min_num = 0
    raw_id_fields = ('product',)
    autocomplete_fields = ['product']

class DetailMoveAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'subtotal')
    search_fields = ['product']

class MoveAdmin(admin.ModelAdmin):
    list_display = ('createDate', 'origin', 'destiny', 'requested', 'checked')
    search_fields = ['origin']
    inlines = [DetailMoveInline]

admin.site.register(Move, MoveAdmin)
admin.site.register(DetailMove, DetailMoveAdmin)