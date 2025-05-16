# core/models.py
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class WorkZone(models.Model):
    nombre = models.CharField(max_length=100)
    numero = models.CharField(max_length=50)
    correo = models.EmailField()
    direccion = models.TextField()

    def __str__(self):
        return self.nombre

class Evento(models.Model):
    workzone = models.ForeignKey(WorkZone, on_delete=models.CASCADE, related_name='eventos')
    tipo = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    problema = models.TextField()
    solucion = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"{self.tipo} - {self.nombre}"
    

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin_global', 'Administrador Global'),
        ('admin_zone', 'Administrador Zona'),
        ('operator', 'Operador'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='operator')
    workzone = models.ForeignKey('WorkZone', null=True, blank=True, on_delete=models.SET_NULL)
    date_of_entry = models.DateField(null=True, blank=True)

#########################################################################################3


class BoxModel(models.Model):
    nombre       = models.CharField(max_length=50, unique=True)
    descripcion  = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class Box(models.Model):
    numero_unico = models.CharField(max_length=20)  # Ya no es unique=True
    modelo       = models.ForeignKey(BoxModel, on_delete=models.CASCADE, related_name='cajas')
    en_bodega    = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.modelo.nombre} — {self.numero_unico}"

    class Meta:
       
        verbose_name = "Caja"
        verbose_name_plural = "Cajas"

class MovementLog(models.Model):
    TIPO_CHOICES = [
        ('salida', 'Salida'),
        ('retorno', 'Retorno'),
    ]
    caja         = models.ForeignKey(Box, on_delete=models.CASCADE, related_name='movimientos')
    usuario      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    fecha_hora   = models.DateTimeField(auto_now_add=True)
    tipo         = models.CharField(max_length=10, choices=TIPO_CHOICES)
    area_destino = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.get_tipo_display()} | {self.caja.numero_unico} @ {self.fecha_hora:%Y-%m-%d %H:%M}"
    

###############################################################

class BoxDeliveryRecord(models.Model):
    caja         = models.ForeignKey(Box, on_delete=models.CASCADE, null=True, blank=True)
    area_destino = models.CharField(max_length=100, blank=True)
    usuario      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    fecha_hora   = models.DateTimeField()  # ❌ Quitamos auto_now_add
    sin_cambios  = models.BooleanField(default=False)

    def __str__(self):
        if self.sin_cambios:
            return f"[Sin cambios] {self.usuario} - {self.fecha_hora.strftime('%d/%m %I:%M %p')}"
        return f"{self.caja} → {self.area_destino} ({self.fecha_hora.strftime('%I:%M %p')})"
