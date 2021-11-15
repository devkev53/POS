from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (
            None, {
                'fields': ('role', 'cui', 'phone', 'gender',)
            }
        ),
    )
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'userCreation']

admin.site.register(User, CustomUserAdmin)

