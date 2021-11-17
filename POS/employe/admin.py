from django.contrib import admin
from .models import Employe

# Register your models here.

@admin.register(Employe)
class EmployeAdmin(admin.ModelAdmin):
    '''Admin View for Employe'''

    list_display = ('__str__', 'store', 'role', 'userCreation', 'userUpdate')
    list_filter = ('store', 'role')
    # inlines = [Inline,]
    # raw_id_fields = ('',)
    # readonly_fields = ('',)
    search_fields = ('user.username', 'user.first_name', 'user.last_name')
    # date_hierarchy = ''
    # ordering = ('',)
