from django.db import models
from datetime import datetime

class Adherent(models.Model):
    CodeAdh = models.CharField(max_length=20, unique=True, blank=True)
    NomAdh = models.CharField(max_length=100)
    PrenomAdh = models.CharField(max_length=100)
    SexeAdh = models.CharField(max_length=10, choices=[('M', 'Masculin'), ('F', 'Féminin')])
    DateAdhesionAdh = models.DateField()
    TelephoneAdh = models.CharField(max_length=20, unique=True)
    EmailAdh = models.EmailField(max_length=100, blank=True, null=True)
    AdresseAdh = models.TextField()
    MontantACotiserAdh = models.DecimalField(max_digits=10, decimal_places=2)
    StatutAdh = models.CharField(max_length=20, choices=[('Actif', 'Actif'), ('Inactif', 'Inactif', ), ('Suspendu', 'Suspendu')])
    ImageAdh = models.ImageField(upload_to='adherents/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.CodeAdh:
            self.CodeAdh = self.generate_codeadh()
        super().save(*args, **kwargs)

    def generate_codeadh(self):
        # Obtenir l'année actuelle
        current_year = datetime.now().year
        # Compter le nombre d'adhérents créés cette année
        adherent_count = Adherent.objects.filter(DateAdhesionAdh__year=current_year).count() + 1
        # Générer le CodeAdh sous la forme ADH+ANNEE+Nombre à trois chiffres
        return f"ADH{current_year}{adherent_count:03d}"

    def __str__(self):
        return f"{self.NomAdh} {self.PrenomAdh}"
