# forms.py
from django import forms
from .models import Adherent  # Assurez-vous que le modèle Adherent est défini dans models.py

class AdherentForm(forms.ModelForm):
    CodeAdh                 = forms.CharField(widget=forms.HiddenInput(attrs={'class': 'form-control'}))
    NomAdh                  = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    PrenomAdh               = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    SexeAdh                 = forms.ChoiceField(
        choices=[('', 'Veuillez sélectionner le sexe de l\'adhérent'),('M', 'Masculin'), ('F', 'Féminin')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    DateAdhesionAdh = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    TelephoneAdh            = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    EmailAdh                = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}),required=False, ) # Permet au champ de ne pas être renseigné
    AdresseAdh              = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    MontantACotiserAdh      = forms.DecimalField(
        max_digits=10, decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    StatutAdh               = forms.ChoiceField(
        choices=[('', 'Veuillez sélectionner le statut de l\'adhérent'),('Actif', 'Actif'), ('Inactif', 'Inactif'), ('Suspendu', 'Suspendu')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    ImageAdh                = forms.ImageField(
        required=False,  # False si l'image est optionnelle
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Adherent
        fields = ['CodeAdh', 'NomAdh', 'PrenomAdh', 'SexeAdh', 'DateAdhesionAdh', 'TelephoneAdh', 'EmailAdh', 'AdresseAdh', 'MontantACotiserAdh', 'StatutAdh', 'ImageAdh']
        widgets = {
            'DateAdhesionAdh': forms.TextInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        # Retirer CodeAdh des arguments si présent
        code_adh = kwargs.pop('code_adh', None)
        super().__init__(*args, **kwargs)
        # Assigner la valeur de CodeAdh si elle est disponible
        if code_adh:
            self.fields['CodeAdh'].initial = code_adh
