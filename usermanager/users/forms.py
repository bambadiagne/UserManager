from django import forms
from .models import Utilisateur
# Create your models here.


class UtilisateurForm(forms.ModelForm):
    nom = forms.CharField(label='nom', max_length=30)
    prenom = forms.CharField(label='prenom', max_length=30)
    identifiant = forms.CharField(label='identifiant', max_length=30)
    email = forms.EmailField(label='email', max_length=254,)
    date_naissance = forms.DateField(label="date"),
    mot_de_passe = forms.CharField(label="mot de passe", max_length=32)
    profile = forms.CharField(label='profile', max_length=30)

    class Meta:
        model = Utilisateur
        fields = ['nom', 'prenom', 'identifiant', 'mot_de_passe', 'profile']
