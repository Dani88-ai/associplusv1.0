from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control'
               }
    )
    )
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control pass-input'
        }
    )
    )


class RegisterForm(UserCreationForm):
    # Champs déjà existants
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control pass-input'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control pass-input'}))

    # Champs boolean pour les rôles
    is_admin = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    is_president = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    is_tresorier = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    is_secretaire = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    is_membre = forms.BooleanField(required=False, widget=forms.CheckboxInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'is_admin', 'is_president', 'is_tresorier', 'is_secretaire', 'is_membre')
