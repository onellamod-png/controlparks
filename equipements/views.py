# On importe render pour afficher les templates HTML et redirect pour rediriger vers une autre page
from django.shortcuts import render, redirect
import json
from django.http import JsonResponse

# On importe les classes (tables) dont on a besoin depuis models.py
from .models import Boitier, CarteSIM, Installation, Technicien, Vehicule, Client, Diagnostic, ModeleBoitier, Operateur

# On importe les formulaires depuis forms.py
from .forms import BoitierForm, CarteSIMForm, ClientForm, VehiculeForm, InstallationForm, DiagnosticForm


# PAGE D'ACCUEIL - Tableau de bord

def accueil(request):
    # Compteurs généraux
    total_boitiers = Boitier.objects.count()
    total_sims = CarteSIM.objects.count()
    total_installations = Installation.objects.filter(date_desinstallation=None).count()
    total_vehicules = Vehicule.objects.count()
    total_diagnostics = Diagnostic.objects.count()

    # Statistiques boîtiers
    boitiers_en_stock = Boitier.objects.filter(etat='stock').count()
    boitiers_installes = Boitier.objects.filter(etat='installe').count()
    boitiers_en_panne = Boitier.objects.filter(etat='panne').count()
    boitiers_retires = Boitier.objects.filter(etat='retire').count()

    # 5 dernières installations
    dernieres_installations = Installation.objects.all()[:5]

    return render(request, 'equipements/accueil.html', {
        'total_boitiers': total_boitiers,
        'total_sims': total_sims,
        'total_installations': total_installations,
        'total_vehicules': total_vehicules,
        'total_diagnostics': total_diagnostics,
        'boitiers_en_stock': boitiers_en_stock,
        'boitiers_installes': boitiers_installes,
        'boitiers_en_panne': boitiers_en_panne,
        'boitiers_retires': boitiers_retires,
        'dernieres_installations': dernieres_installations,
    })

# BOÎTIERS
def liste_boitiers(request):
    query = request.GET.get('q', '')
    if query:
        boitiers = Boitier.objects.filter(numero_serie__icontains=query)
    else:
        boitiers = Boitier.objects.all()
    return render(request, 'equipements/boitiers/liste.html', {
        'boitiers': boitiers,
        'query': query
    })

def ajouter_boitier(request):
    if request.method == 'POST':
        form = BoitierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_boitiers')
    else:
        form = BoitierForm()
    return render(request, 'equipements/boitiers/ajouter.html', {
        'form': form
    })

def modifier_boitier(request, id):
    boitier = Boitier.objects.get(id=id)
    if request.method == 'POST':
        form = BoitierForm(request.POST, instance=boitier)
        if form.is_valid():
            form.save()
            return redirect('liste_boitiers')
    else:
        form = BoitierForm(instance=boitier)
    return render(request, 'equipements/boitiers/modifier.html', {
        'form': form,
        'boitier': boitier
    })

def supprimer_boitier(request, id):
    boitier = Boitier.objects.get(id=id)
    if request.method == 'POST':
        boitier.delete()
        return redirect('liste_boitiers')
    return render(request, 'equipements/boitiers/supprimer.html', {
        'boitier': boitier
    })

def historique_boitier(request, id):
    boitier = Boitier.objects.get(id=id)
    installations = Installation.objects.filter(boitier=boitier)
    return render(request, 'equipements/boitiers/historique.html', {
        'boitier': boitier,
        'installations': installations,
    })


# CARTES SIM
def liste_sims(request):
    query = request.GET.get('q', '')
    if query:
        sims = CarteSIM.objects.filter(iccid__icontains=query)
    else:
        sims = CarteSIM.objects.all()
    return render(request, 'equipements/sims/liste.html', {
        'sims': sims,
        'query': query
    })

def ajouter_sim(request):
    if request.method == 'POST':
        form = CarteSIMForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_sims')
    else:
        form = CarteSIMForm()
    return render(request, 'equipements/sims/ajouter.html', {
        'form': form
    })

def modifier_sim(request, id):
    sim = CarteSIM.objects.get(id=id)
    if request.method == 'POST':
        form = CarteSIMForm(request.POST, instance=sim)
        if form.is_valid():
            form.save()
            return redirect('liste_sims')
    else:
        form = CarteSIMForm(instance=sim)
    return render(request, 'equipements/sims/modifier.html', {
        'form': form,
        'sim': sim
    })

def supprimer_sim(request, id):
    sim = CarteSIM.objects.get(id=id)
    if request.method == 'POST':
        sim.delete()
        return redirect('liste_sims')
    return render(request, 'equipements/sims/supprimer.html', {
        'sim': sim
    })


# CLIENTS
def liste_clients(request):
    query = request.GET.get('q', '')
    if query:
        clients = Client.objects.filter(nom__icontains=query) | Client.objects.filter(prenom__icontains=query)
    else:
        clients = Client.objects.all()
    return render(request, 'equipements/clients/liste.html', {
        'clients': clients,
        'query': query
    })

def ajouter_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_clients')
    else:
        form = ClientForm()
    return render(request, 'equipements/clients/ajouter.html', {
        'form': form
    })

def modifier_client(request, id):
    client = Client.objects.get(id=id)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('liste_clients')
    else:
        form = ClientForm(instance=client)
    return render(request, 'equipements/clients/modifier.html', {
        'form': form,
        'client': client
    })

def supprimer_client(request, id):
    client = Client.objects.get(id=id)
    if request.method == 'POST':
        client.delete()
        return redirect('liste_clients')
    return render(request, 'equipements/clients/supprimer.html', {
        'client': client
    })


# VÉHICULES
def liste_vehicules(request):
    query = request.GET.get('q', '')
    if query:
        vehicules = Vehicule.objects.filter(plaque__icontains=query)
    else:
        vehicules = Vehicule.objects.all()
    return render(request, 'equipements/vehicules/liste.html', {
        'vehicules': vehicules,
        'query': query
    })

def ajouter_vehicule(request):
    if request.method == 'POST':
        form = VehiculeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_vehicules')
    else:
        form = VehiculeForm()
    return render(request, 'equipements/vehicules/ajouter.html', {
        'form': form
    })

def modifier_vehicule(request, id):
    vehicule = Vehicule.objects.get(id=id)
    if request.method == 'POST':
        form = VehiculeForm(request.POST, instance=vehicule)
        if form.is_valid():
            form.save()
            return redirect('liste_vehicules')
    else:
        form = VehiculeForm(instance=vehicule)
    return render(request, 'equipements/vehicules/modifier.html', {
        'form': form,
        'vehicule': vehicule
    })

def supprimer_vehicule(request, id):
    vehicule = Vehicule.objects.get(id=id)
    if request.method == 'POST':
        vehicule.delete()
        return redirect('liste_vehicules')
    return render(request, 'equipements/vehicules/supprimer.html', {
        'vehicule': vehicule
    })


# INSTALLATIONS
def liste_installations(request):
    query = request.GET.get('q', '')
    if query:
        installations = Installation.objects.filter(boitier__numero_serie__icontains=query) | Installation.objects.filter(vehicule__plaque__icontains=query)
    else:
        installations = Installation.objects.all()
    return render(request, 'equipements/installations/liste.html', {
        'installations': installations,
        'query': query
    })

def ajouter_installation(request):
    if request.method == 'POST':
        form = InstallationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_installations')
    else:
        form = InstallationForm()
    return render(request, 'equipements/installations/ajouter.html', {
        'form': form,
        'modeles': ModeleBoitier.objects.all(),
        'operateurs': Operateur.objects.all(),
        'clients': Client.objects.all(),
    })

def modifier_installation(request, id):
    installation = Installation.objects.get(id=id)
    if request.method == 'POST':
        form = InstallationForm(request.POST, instance=installation)
        if form.is_valid():
            form.save()
            return redirect('liste_installations')
    else:
        form = InstallationForm(instance=installation)
    return render(request, 'equipements/installations/modifier.html', {
        'form': form,
        'installation': installation
    })

def supprimer_installation(request, id):
    installation = Installation.objects.get(id=id)
    if request.method == 'POST':
        installation.delete()
        return redirect('liste_installations')
    return render(request, 'equipements/installations/supprimer.html', {
        'installation': installation
    })


# DIAGNOSTICS
def liste_diagnostics(request):
    query = request.GET.get('q', '')
    if query:
        diagnostics = Diagnostic.objects.filter(installation__boitier__numero_serie__icontains=query)
    else:
        diagnostics = Diagnostic.objects.all()
    return render(request, 'equipements/diagnostics/liste.html', {
        'diagnostics': diagnostics,
        'query': query
    })

def ajouter_diagnostic(request):
    if request.method == 'POST':
        form = DiagnosticForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_diagnostics')
        else:
            print(form.errors)
    else:
        form = DiagnosticForm()
    return render(request, 'equipements/diagnostics/ajouter.html', {
        'form': form
    })

def modifier_diagnostic(request, id):
    diagnostic = Diagnostic.objects.get(id=id)
    if request.method == 'POST':
        form = DiagnosticForm(request.POST, instance=diagnostic)
        if form.is_valid():
            form.save()
            return redirect('liste_diagnostics')
    else:
        form = DiagnosticForm(instance=diagnostic)
    return render(request, 'equipements/diagnostics/modifier.html', {
        'form': form,
        'diagnostic': diagnostic
    })

def supprimer_diagnostic(request, id):
    diagnostic = Diagnostic.objects.get(id=id)
    if request.method == 'POST':
        diagnostic.delete()
        return redirect('liste_diagnostics')
    return render(request, 'equipements/diagnostics/supprimer.html', {
        'diagnostic': diagnostic
    })

# HISTORIQUE
def historique_boitier(request, id):
    boitier = Boitier.objects.get(id=id)
    installations = Installation.objects.filter(boitier=boitier)
    return render(request, 'equipements/boitiers/historique.html', {
        'boitier': boitier,
        'installations': installations,
    })


# APIs POUR AJOUT RAPIDE
def api_ajouter_boitier(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        boitier = Boitier.objects.create(
            numero_serie=data['numero_serie'],
            modele_id=data['modele_id'],
            etat='stock'
        )
        return JsonResponse({'id': boitier.id, 'label': boitier.numero_serie})

def api_ajouter_sim(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        sim = CarteSIM.objects.create(
            iccid=data['iccid'],
            numero_telephone=data['numero_telephone'],
            operateur_id=data['operateur_id'],
            etat='active'
        )
        return JsonResponse({'id': sim.id, 'label': sim.iccid})

def api_ajouter_vehicule(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        vehicule = Vehicule.objects.create(
            plaque=data['plaque'],
            marque=data['marque'],
            modele=data['modele'],
            client_id=data['client_id'] if data['client_id'] else None
        )
        return JsonResponse({'id': vehicule.id, 'label': vehicule.plaque})

def api_ajouter_technicien(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        technicien = Technicien.objects.create(
            nom=data['nom'],
            prenom=data['prenom'],
            telephone=data['telephone'],
            email=data['email'],
        )
        return JsonResponse({'id': technicien.id, 'label': f"{technicien.nom} {technicien.prenom}"})
def api_ajouter_client(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        client = Client.objects.create(
            nom=data['nom'],
            prenom=data['prenom'],
            telephone=data['telephone'],
            email=data['email'],
        )
        return JsonResponse({'id': client.id, 'label': f"{client.nom} {client.prenom}"})