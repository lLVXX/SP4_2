from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, WorkZone, Evento

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'user_type', 'email', 'workzone')
    fieldsets = UserAdmin.fieldsets + (
        ('Rol y Zona', {'fields': ('user_type', 'workzone')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Rol y Zona', {'fields': ('user_type', 'workzone')}),
    )

@admin.register(WorkZone)
class WorkZoneAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'numero', 'correo', 'direccion')

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'workzone', 'fecha')
    list_filter = ('tipo', 'workzone')
