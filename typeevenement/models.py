from django.db import models




# Create your models here.
class TyptEvenement(models.Model):
    LibelleEvenement = models.CharField(max_length=255)
    MontantAPayer = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    observation = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.LibelleEvenement
    