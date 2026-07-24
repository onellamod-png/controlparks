from django import forms
from .models import Boitier, ModeleBoitier, CarteSIM, Operateur,Client,Vehicule,Installation,Diagnostic
class BoitierForm(forms.ModelForm):
    class Meta:
        model = Boitier
        fields = ['numero_serie', 'modele', 'etat', 'date_achat']
        widgets = {
            'date_achat': forms.DateInput(attrs={'type': 'date'}),
        }
        

class CarteSIMForm(forms.ModelForm):
    class Meta:
        model = CarteSIM
        fields = ['numero_telephone', 'iccid', 'operateur', 'etat', 'date_activation']
        widgets = {
            'date_activation': forms.DateInput(attrs={'type': 'date'}),
        }

        

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['nom', 'prenom', 'telephone', 'email']


class VehiculeForm(forms.ModelForm):
    class Meta:
        model = Vehicule
        fields = ['plaque', 'marque', 'modele', 'client']

class InstallationForm(forms.ModelForm):
    class Meta:
        model = Installation
        fields = ['boitier', 'carte_sim', 'vehicule', 'technicien', 'date_installation', 'commentaire']
        widgets = {
            'date_installation': forms.DateInput(attrs={'type': 'date'}),
        }

class DiagnosticForm(forms.ModelForm):
    class Meta:
        model = Diagnostic
        fields = ['installation', 'defauts', 'origine', 'commentaire', 'signale_par']
        widgets = {
            'defauts': forms.CheckboxSelectMultiple(attrs={'style': 'margin-right: 8px;'}),
        }
        