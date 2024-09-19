from django import forms
from .models import Cotisation
from adherent.models import Adherent

class CotisationForm(forms.ModelForm):
    # Personnalisation des widgets pour un meilleur contrôle de l'interface utilisateur
    MoisCotisation = forms.ChoiceField(
        choices=[('', 'Veuillez sélectionner le mois de la cotisation'),('Janvier', 'Janvier'), ('Février', 'Février'),('Mars', 'Mars'),('Avril', 'Avril'),('Mai', 'Mai'),('Juin', 'Juin'),('Juillet', 'Juillet'),('Août', 'Août'),('Septembre', 'Septembre'),('Octobre', 'Octobre'),('Novembre', 'Novembre'),('Décembre', 'Décembre')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    DatePaiement = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control','type': 'date'}))
    AnneeConcernee = forms.IntegerField(widget=forms.NumberInput(attrs={'min': 2000, 'max': 2100}))
    MontantCotise = forms.DecimalField(widget=forms.NumberInput(attrs={'step': 0.01}))

    class Meta:
        model = Cotisation
        fields = ['Adherent', 'DatePaiement','MoisCotisation','AnneeConcernee', 'MontantCotise']
        widget = {
            'DatePaiement': forms.TextInput(attrs={'type': 'date'}),

        }
        labels = {
            'Adherent': 'Nom | Prénom',
            'DatePaiement': 'Date du paiement de la cotisation',
            'MoisCotisation': 'Mois de la cotisation',
            'AnneeConcernee': 'Année concernée',
            'MontantCotise': 'Montant cotisé',
        }


    def __init__(self, *args, **kwargs):
        super(CotisationForm, self).__init__(*args, **kwargs)
        # Filtrer les adhérents actifs et inactif uniquement
        self.fields['Adherent'].queryset = Adherent.objects.filter(StatutAdh__in=['Actif', 'Inactif'])

        # Personnaliser les widgets pour une meilleure apparence
        self.fields['Adherent'].widget.attrs.update({'class': 'form-control'})
        self.fields['DatePaiement'].widget.attrs.update({'class': 'form-control','type': 'date'})
        self.fields['MoisCotisation'].widget.attrs.update({'class': 'form-control'})
        self.fields['AnneeConcernee'].widget.attrs.update({'class': 'form-control'})
        self.fields['MontantCotise'].widget.attrs.update({'class': 'form-control'})
