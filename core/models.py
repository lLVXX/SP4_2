# core/models.py
from django.db import models
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

