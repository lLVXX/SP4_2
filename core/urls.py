from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('Ingreso/', views.Ingreso, name='Ingreso'),
    path('logout/', views.logout_view, name='logout'),

    # Operador
    path('InicioOperadorHospital/', views.InicioOperadorHospital, name='InicioOperadorHospital'),
    path('InicioOperadorClinica/', views.InicioOperadorClinica, name='InicioOperadorClinica'),
    path('cambiar_contrasena/', views.cambiar_contrasena, name='cambiar_contrasena'),

    # Admin Zona
    path('InicioAdminHospital/', views.InicioAdminHospital, name='InicioAdminHospital'),
    path('InicioAdminClinica/', views.InicioAdminClinica, name='InicioAdminClinica'),
    path('HospitalGestionUsuarios/', views.HospitalGestionUsuarios, name='HospitalGestionUsuarios'),

    # Admin Global
    path('InicioAdminGl/', views.InicioAdminGl, name='InicioAdminGl'),
    path('admin_global/workzones/crear/', views.crear_workzone, name='crear_workzone'),
    path('admin_global/workzones/listar/', views.listar_workzones, name='listar_workzones'),
    path('admin_global/admins/crear/', views.crear_admin_zone, name='crear_admin_zone'),

    # Inventario
    path('inventario/', views.inventario, name='inventario'),
    path('fin-de-turno/', views.fin_de_turno, name='fin_de_turno'),
    path('fin-de-turno/<int:pk>/resumen/', views.fin_de_turno_resumen, name='fin_de_turno_resumen'),
    path('reportes-fin-turno/', views.listar_reportes, name='listar_reportes'),
]