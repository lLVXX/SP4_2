from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, WorkZone, Evento, BoxModel, Box, MovementLog

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

#####################################################################

@admin.register(BoxModel)
class BoxModelAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)

@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = ('numero_de_serie', 'numero_unico', 'modelo', 'en_bodega')  # <-- actualizado
    list_filter  = ('modelo', 'en_bodega')
    search_fields = ('numero_de_serie', 'numero_unico', 'modelo__nombre')  # <-- actualizado

@admin.register(MovementLog)
class MovementLogAdmin(admin.ModelAdmin):
    list_display   = ('caja', 'tipo', 'usuario', 'area_destino', 'fecha_hora')
    list_filter    = ('tipo', 'fecha_hora')
    search_fields  = ('caja__numero_unico', 'caja__numero_de_serie', 'area_destino', 'usuario__username')  # <-- actualizado
    readonly_fields = ('fecha_hora', 'usuario', 'tipo')

    def save_model(self, request, obj, form, change):
        if not change:
            if obj.caja.en_bodega:
                obj.tipo = 'salida'
                obj.caja.en_bodega = False
            else:
                obj.tipo = 'retorno'
                obj.caja.en_bodega = True
            obj.usuario = request.user
            obj.caja.save()
        super().save_model(request, obj, form, change)
