# core/forms.py

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model

from .models import *

Usuario = get_user_model()

################################################ USUARIOS ################################################

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
    )

class OperadorCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'operador'
        user.workzone = 'hospital'
        if commit:
            user.save()
        return user

################################################ ZONA DE TRABAJO ################################################

class WorkZoneForm(forms.ModelForm):
    class Meta:
        model = WorkZone
        fields = ['nombre', 'numero', 'correo', 'direccion']

class AdminZoneCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'workzone']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'admin_zone'
        user.set_password('12345678')  # Clave por defecto
        if commit:
            user.save()
        return user

###################################  REGISTROS BODEGA ################################

class MovementLogForm(forms.ModelForm):
    class Meta:
        model = MovementLog
        fields = ['caja', 'area_destino']
        widgets = {
            'area_destino': forms.TextInput(attrs={'placeholder': 'Ej. pabellón'})
        }

#############################################################

class AddBoxForm(forms.ModelForm):
    class Meta:
        model = Box
        fields = ['modelo', 'numero_unico', 'numero_de_serie']  # <-- actualizado
        labels = {
            'numero_unico': 'Número de Caja',
            'numero_de_serie': 'Número de Serie',
        }

    def clean_numero_de_serie(self):
        numero = self.cleaned_data.get('numero_de_serie')
        if Box.objects.filter(numero_de_serie=numero).exists():
            raise forms.ValidationError("Este número de serie ya está registrado.")
        return numero

class BoxDeliveryForm(forms.Form):
    modelo = forms.ModelChoiceField(queryset=BoxModel.objects.all(), label='Modelo')
    numero_unico = forms.ChoiceField(label='Número de caja', required=False)
    area_destino = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Ej. FARMACIA'})
    )
    hora_entrega = forms.TimeField(
        label="Hora de entrega",
        widget=forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
        required=False
    )

    def __init__(self, *args, **kwargs):
        modelo_id = kwargs.pop('modelo_id', None)
        super().__init__(*args, **kwargs)

        if modelo_id:
            cajas = Box.objects.filter(modelo_id=modelo_id, en_bodega=True).order_by('numero_unico')
            self.fields['numero_unico'].choices = [(c.numero_unico, c.numero_unico) for c in cajas]
            self.fields['numero_unico'].required = True
            self.fields['area_destino'].required = True
            self.fields['hora_entrega'].required = True
        else:
            self.fields['numero_unico'].choices = []

############# FIN DE TURNO ###############

class ConfirmarFinTurnoForm(forms.Form):
    confirmar = forms.BooleanField(label='Confirmo que deseo finalizar el turno')
