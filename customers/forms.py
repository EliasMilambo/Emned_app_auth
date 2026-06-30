# forms.py
from django import forms
from django.contrib.auth import get_user_model
from customers.models import Customer

User = get_user_model()

# 1. TON FORMULAIRE EXISTANT (Gestion des clients du CRM)
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'telephone', 'status']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
            'telephone': 'Telephone',
            'status': 'Statut',
        }

# 2. LE NOUVEAU FORMULAIRE (Inscription des Utilisateurs au Dashboard)
class UserRegisterForm(forms.ModelForm):
    # Ajout du champ de mot de passe avec le bon widget d'affichage
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'username': "Nom d'utilisateur *",
            'first_name': 'Prénom *',
            'last_name': 'Nom *',
            'email': 'Adresse email *',
            'phone': 'Téléphone',
        }
