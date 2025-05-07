# core/forms.py

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model

from .models import WorkZone, CustomUser



Usuario = get_user_model()

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