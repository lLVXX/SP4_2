from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.conf import settings
from django.utils.timezone import now, make_aware
from django.contrib.auth import get_user_model
from django.utils.dateparse import parse_date
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from datetime import datetime

from .forms import (
    WorkZoneForm,
    AdminZoneCreationForm,
    CustomLoginForm,
    AddBoxForm,
    BoxDeliveryForm,
    MovementLogForm
)
from .models import WorkZone, BoxModel, Box, BoxDeliveryRecord

Usuario = get_user_model()

# ============================ Helpers ============================

def is_admin_or_operator(u):
    return u.is_authenticated and u.user_type in ('admin_zone', 'operador')

def is_admingl(user):
    return user.is_authenticated and user.user_type == 'admin_global'

def is_admin_zone(user):
    return user.is_authenticated and user.user_type == 'admin_zone'

def redirect_user_based_on_role(user):
    if user.user_type == 'operador':
        if user.workzone and user.workzone.nombre.lower() == 'hospital':
            return redirect('InicioOperadorHospital')
        elif user.workzone and user.workzone.nombre.lower() == 'clinica':
            return redirect('InicioOperadorClinica')
    elif user.user_type == 'admin_zone':
        if user.workzone and user.workzone.nombre.lower() == 'hospital':
            return redirect('InicioAdminHospital')
        elif user.workzone and user.workzone.nombre.lower() == 'clinica':
            return redirect('InicioAdminClinica')
    elif user.user_type == 'admin_global':
        return redirect('InicioAdminGl')
    return redirect('Ingreso')

# ============================ Autenticación ============================

def home(request):
    if request.user.is_authenticated:
        return redirect_user_based_on_role(request.user)
    return render(request, 'core/home.html')

def Ingreso(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect_user_based_on_role(user)
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = CustomLoginForm()
    return render(request, 'core/Ingreso.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('Ingreso')

# ============================ Vistas Operador ============================

@login_required
def InicioOperadorHospital(request):
    if request.user.user_type != 'operador' or request.user.workzone.nombre.lower() != 'hospital':
        return redirect('Ingreso')
    return render(request, 'core/Operador/InicioOperadorHospital.html')

@login_required
def InicioOperadorClinica(request):
    if request.user.user_type != 'operador' or request.user.workzone.nombre.lower() != 'clinica':
        return redirect('Ingreso')
    return render(request, 'core/Operador/InicioOperadorClinica.html')

@login_required
def cambiar_contrasena(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Contraseña actualizada correctamente!')
            return redirect_user_based_on_role(request.user)
        else:
            messages.error(request, 'Por favor corrija los errores.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'core/Operador/cambiar_contrasena.html', {'form': form})

# ============================ Vistas Admin por Zona ============================

@login_required
def InicioAdminHospital(request):
    if not is_admin_zone(request.user) or request.user.workzone.nombre.lower() != 'hospital':
        return redirect('Ingreso')
    return render(request, 'core/Admin/InicioAdminHospital.html')

@login_required
def InicioAdminClinica(request):
    if not is_admin_zone(request.user) or request.user.workzone.nombre.lower() != 'clinica':
        return redirect('Ingreso')
    return render(request, 'core/Admin/InicioAdminClinica.html')

@login_required
def HospitalGestionUsuarios(request):
    if not is_admin_zone(request.user) or request.user.workzone.nombre.lower() != 'hospital':
        return redirect('Ingreso')

    if request.method == 'POST':
        if 'delete_user' in request.POST:
            user_id = request.POST.get('delete_user')
            user = get_object_or_404(Usuario, id=user_id, user_type='operador', workzone=request.user.workzone)
            user.delete()
            messages.success(request, f"Operador '{user.username}' eliminado correctamente.")
            return redirect('HospitalGestionUsuarios')

        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        date_of_entry = request.POST.get('date_of_entry')
        password = '12345678'

        if not username:
            messages.error(request, "El nombre de usuario es requerido.")
        elif Usuario.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya existe.")
        else:
            user = Usuario.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=password,
                user_type='operador',
                workzone=request.user.workzone
            )
            user.date_of_entry = parse_date(date_of_entry) if date_of_entry else None
            user.save()
            messages.success(request, f"Operador '{username}' creado exitosamente con contraseña por defecto.")
            return redirect('HospitalGestionUsuarios')

    operadores = Usuario.objects.filter(user_type='operador', workzone=request.user.workzone)
    return render(request, 'core/Admin/HospitalGestionUsuarios.html', {'operadores': operadores})

# ============================ Vistas Admin Global ============================

@login_required
@user_passes_test(is_admingl)
def InicioAdminGl(request):
    return render(request, 'core/AdminGL/InicioAdminGl.html')

@login_required
@user_passes_test(is_admingl)
def crear_workzone(request):
    if request.method == 'POST':
        form = WorkZoneForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Zona de trabajo creada exitosamente.")
            return redirect('listar_workzones')
    else:
        form = WorkZoneForm()
    return render(request, 'core/AdminGL/crear_workzone.html', {'form': form})

@login_required
@user_passes_test(is_admingl)
def crear_admin_zone(request):
    if request.method == 'POST':
        form = AdminZoneCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Administrador de zona creado exitosamente.")
            return redirect('crear_admin_zone')
    else:
        form = AdminZoneCreationForm()
    return render(request, 'core/AdminGL/crear_admin_zone.html', {'form': form})

@login_required
@user_passes_test(is_admingl)
def listar_workzones(request):
    zonas = WorkZone.objects.all()
    return render(request, 'core/AdminGL/listar_workzones.html', {'zonas': zonas})

# ============================ Inventario ============================


@login_required
@user_passes_test(is_admin_or_operator)
def inventario(request):
    modelos = BoxModel.objects.all().order_by('nombre')

    tabla_por_modelo = []
    for m in modelos:
        cajas = m.cajas.filter(en_bodega=True)
        numeros = [c.numero_unico for c in cajas]
        tabla_por_modelo.append({
            'modelo': m.nombre,
            'numeros': numeros,  # lista para iterar
            'total': cajas.count()
        })

    add_box_form = AddBoxForm()
    modelo_id = None

    if request.method == 'POST':
        if 'add_box' in request.POST:
            add_box_form = AddBoxForm(request.POST)
            if add_box_form.is_valid():
                new_box = add_box_form.save(commit=False)
                if Box.objects.filter(modelo=new_box.modelo, numero_unico=new_box.numero_unico, en_bodega=True).exists():
                    messages.error(request, "Ya existe una caja en bodega con ese modelo y número.")
                else:
                    new_box.en_bodega = True
                    new_box.save()
                    messages.success(request, "Caja agregada exitosamente.")
                return redirect('inventario')

        elif 'filtrar_modelo' in request.POST:
            modelo_id = request.POST.get('modelo')
            delivery_form = BoxDeliveryForm(request.POST, modelo_id=modelo_id)

        elif 'register_delivery' in request.POST:
            modelo_id = request.POST.get('modelo')
            delivery_form = BoxDeliveryForm(request.POST, modelo_id=modelo_id)
            if delivery_form.is_valid():
                modelo = delivery_form.cleaned_data['modelo']
                numero = delivery_form.cleaned_data['numero_unico']
                area = delivery_form.cleaned_data['area_destino']
                hora = delivery_form.cleaned_data['hora_entrega']

                fecha = now().date()
                fecha_hora = make_aware(datetime.combine(fecha, hora))

                try:
                    caja = Box.objects.get(modelo=modelo, numero_unico=numero, en_bodega=True)
                except Box.DoesNotExist:
                    messages.error(request, "La caja seleccionada no está disponible.")
                else:
                    BoxDeliveryRecord.objects.create(
                        caja=caja,
                        area_destino=area,
                        usuario=request.user,
                        sin_cambios=False,
                        fecha_hora=fecha_hora
                    )
                    caja.en_bodega = False
                    caja.save()
                    messages.success(request, "Entrega registrada.")
                return redirect('inventario')

        elif 'sin_cambios' in request.POST:
            today = now().date()
            already_exists = BoxDeliveryRecord.objects.filter(
                usuario=request.user,
                sin_cambios=True,
                fecha_hora__date=today
            ).exists()
            if already_exists:
                messages.info(request, "Ya registraste 'Sin cambios' hoy.")
            else:
                BoxDeliveryRecord.objects.create(
                    usuario=request.user,
                    sin_cambios=True,
                    fecha_hora=now()
                )
                messages.success(request, "Fin de turno registrado sin entregas.")
            return redirect('inventario')

    else:
        delivery_form = BoxDeliveryForm()

    historial = BoxDeliveryRecord.objects.filter(
        usuario=request.user,
        fecha_hora__date=now().date()
    ).order_by('-fecha_hora')

    return render(request, 'core/inventario.html', {
        'tabla_por_modelo': tabla_por_modelo,
        'add_box_form': add_box_form,
        'delivery_form': delivery_form,
        'historial': historial,
    })