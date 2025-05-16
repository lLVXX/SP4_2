# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Public views
    path('', views.home, name='home'),
    path('Ingreso/', views.Ingreso, name='Ingreso'),
    path('logout/', views.logout_view, name='logout'),

    # Operador views
    path('InicioOperadorHospital/', views.InicioOperadorHospital, name='InicioOperadorHospital'),
    path('InicioOperadorClinica/', views.InicioOperadorClinica, name='InicioOperadorClinica'),
    path('cambiar_contrasena/', views.cambiar_contrasena, name='cambiar_contrasena'),

    # Admin Zona views
    path('InicioAdminHospital/', views.InicioAdminHospital, name='InicioAdminHospital'),
    path('InicioAdminClinica/', views.InicioAdminClinica, name='InicioAdminClinica'),
    path('HospitalGestionUsuarios/', views.HospitalGestionUsuarios, name='HospitalGestionUsuarios'),

    # Admin Global views
    path('InicioAdminGl/', views.InicioAdminGl, name='InicioAdminGl'),
    path('admin_global/workzones/crear/', views.crear_workzone, name='crear_workzone'),
    path('admin_global/workzones/listar/', views.listar_workzones, name='listar_workzones'),
    path('admin_global/admins/crear/', views.crear_admin_zone, name='crear_admin_zone'),

    # Inventario 
    
    path('inventario/', views.inventario,          name='inventario'),
   


]
