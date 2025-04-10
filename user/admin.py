from django.contrib import admin

from user.models import CustomUser

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """
    Admin interface for the CustomUser model.
    """
    list_display = ('email', 'nome', 'sobrenome', 'sexo', 'genero', 'is_active',)
    search_fields = ('email',)
    list_filter = ('is_staff', 'is_active')
    ordering = ('email',)