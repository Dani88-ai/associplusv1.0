""" from django.db import models
from adherent.models import Adherent
from django.db.models import Sum

# Create your models here.

class Cotisation(models.Model):
    # Utiliser une chaîne de caractères pour éviter l'importation circulaire
    Adherent = models.ForeignKey('adherent.Adherent', on_delete=models.CASCADE)
    DatePaiement = models.DateField()
    MoisCotisation = models.CharField(max_length=100)
    AnneeConcernee = models.IntegerField()
    MontantCotise = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def reste_a_cotiser(self):
        # Calculer le total des cotisations pour l'adhérent, le mois et l'année
        total_cotise = Cotisation.objects.filter(
            Adherent=self.Adherent,
            MoisCotisation=self.MoisCotisation,
            AnneeConcernee=self.AnneeConcernee
        ).aggregate(total=Sum('MontantCotise'))['total'] or 0

        # Calculer le reste à cotiser en soustrayant le total cotisé du montant total à cotiser
        return self.Adherent.MontantACotiserAdh - total_cotise

    def save(self, *args, **kwargs):
        # Mettre à jour automatiquement le montant restant à cotiser après chaque sauvegarde de cotisation
        super().save(*args, **kwargs)
        self.Adherent.MontantACotiserAdh = self.reste_a_cotiser
        self.Adherent.save()

    def __str__(self):
        return f"Cotisation de {self.Adherent.NomAdh} {self.Adherent.PrenomAdh} pour {self.MoisCotisation} {self.AnneeConcernee}"


    
 """


from django.db import models
from adherent.models import Adherent
from django.db.models import Sum

class Cotisation(models.Model):
    Adherent = models.ForeignKey('adherent.Adherent', on_delete=models.CASCADE)
    DatePaiement = models.DateField()
    MoisCotisation = models.CharField(max_length=100, choices=[('Janvier', 'Janvier'), ('Février', 'Février'),('Mars', 'Mars'),('Avril', 'Avril'),('Mai', 'Mai'),('Juin', 'Juin'),('Juillet', 'Juillet'),('Août', 'Août'),('Septembre', 'Septembre'),('Octobre', 'Octobre'),('Novembre', 'Novembre'),('Décembre', 'Décembre')])
    AnneeConcernee = models.IntegerField()
    MontantCotise = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_cotise(self):
        """
        Retourne le total cotisé pour l'adhérent pour une année donnée.
        """
        total = Cotisation.objects.filter(
            Adherent=self.Adherent,
            AnneeConcernee=self.AnneeConcernee
        ).aggregate(total=Sum('MontantCotise'))['total'] or 0
        return total

    @property
    def reste_a_cotiser(self):
        """
        Calcule le montant restant à cotiser en soustrayant le total des cotisations
        du montant initial à cotiser.
        """
        return self.Adherent.MontantACotiserAdh - self.total_cotise

    def __str__(self):
        return f"Cotisation de {self.Adherent.NomAdh} {self.Adherent.PrenomAdh} pour {self.MoisCotisation} {self.AnneeConcernee}"
