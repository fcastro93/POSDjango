from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from menu.forms import CustomUserCreationForm, CustomUserChangeForm
from .models import UnidadMedida, Producto, CustomUser

admin.site.register(UnidadMedida)
admin.site.register(Producto)


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('username', 'password', 'direct_boss', 'indirect_boss', 'creator_boss')


admin.site.register(CustomUser, CustomUserAdmin)
