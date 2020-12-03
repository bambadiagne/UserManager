from django.db import models

# Create your models here.


class Utilisateur(models.Model):
    id_utilisateur = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=30)
    prenom = models.CharField(max_length=30)
    identifiant=models.CharField(max_length=30)
    email=models.EmailField(max_length = 254,)
    date_naissance= models.DateField() 
    mot_de_passe=models.CharField(max_length=32)
    profile= models.CharField(max_length=30)
