from django.db import models
from django.contrib.auth.models import AbstractUser




# Create your models here.
class User(AbstractUser):
    is_admin = models.BooleanField('Administrateur', default=False)
    is_tresorier = models.BooleanField('Trésorier', default=False)
    is_president = models.BooleanField('Président', default=False)
    is_membre = models.BooleanField('Membre', default=False)
    is_secretaire = models.BooleanField('Secrétaire', default=False)
