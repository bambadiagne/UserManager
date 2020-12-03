from django import forms

# Create your models here.


class Utilisateur(forms.form):
    nom = forms.CharField(label='nom',max_length=30)
    prenom = forms.CharField(label='prenom',max_length=30)
    identifiant=forms.CharField(label='identifiant',max_length=30)
    email=forms.EmailField(label='email',max_length = 254,)
    date_naissance= forms.DateField() 
    mot_de_passe=forms.CharField(max_length=32)
    profile= forms.CharField(max_length=30)
