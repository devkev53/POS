from django.contrib import admin
from .models import Employe
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class UserInline(admin.TabularInline):
    '''Tabular Inline View for User'''

    model = Employe
    min_num = 1
    # autocomplete_fields = ('username',)

@admin.register(Employe)
class EmployeAdmin(admin.ModelAdmin):
    '''Admin View for Employe'''

    list_display = ('__str__', 'store', 'role', 'userCreation', 'userUpdate')
    list_filter = ('store', 'role')
    # inlines = [UserInline,]
    # raw_id_fields = ('',)
    # readonly_fields = ('',)
    search_fields = ('user.username', 'user.first_name', 'user.last_name')
    # date_hierarchy = ''
    # ordering = ('',)

    # Definimos que se muestren solo nuestra tienda
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            kwargs['queryset'] = User.objects.filter(employe=None)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


