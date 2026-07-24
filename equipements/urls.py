from django.urls import path
from . import views

urlpatterns = [
    # Accueil
    path('', views.accueil, name='accueil'),

    # Boîtiers
    path('boitiers/', views.liste_boitiers, name='liste_boitiers'),
    path('boitiers/ajouter/', views.ajouter_boitier, name='ajouter_boitier'),
    path('boitiers/<int:id>/modifier/', views.modifier_boitier, name='modifier_boitier'),
    path('boitiers/<int:id>/supprimer/', views.supprimer_boitier, name='supprimer_boitier'),

    # Cartes SIM
    path('sims/', views.liste_sims, name='liste_sims'),
    path('sims/ajouter/', views.ajouter_sim, name='ajouter_sim'),
    path('sims/<int:id>/modifier/', views.modifier_sim, name='modifier_sim'),
    path('sims/<int:id>/supprimer/', views.supprimer_sim, name='supprimer_sim'),

    # Clients
    path('clients/', views.liste_clients, name='liste_clients'),
    path('clients/ajouter/', views.ajouter_client, name='ajouter_client'),
    path('clients/<int:id>/modifier/', views.modifier_client, name='modifier_client'),
    path('clients/<int:id>/supprimer/', views.supprimer_client, name='supprimer_client'),

    # Véhicules
    path('vehicules/', views.liste_vehicules, name='liste_vehicules'),
    path('vehicules/ajouter/', views.ajouter_vehicule, name='ajouter_vehicule'),
    path('vehicules/<int:id>/modifier/', views.modifier_vehicule, name='modifier_vehicule'),
    path('vehicules/<int:id>/supprimer/', views.supprimer_vehicule, name='supprimer_vehicule'),

    # Installations
    path('installations/', views.liste_installations, name='liste_installations'),
    path('installations/ajouter/', views.ajouter_installation, name='ajouter_installation'),
    path('installations/<int:id>/modifier/', views.modifier_installation, name='modifier_installation'),
    path('installations/<int:id>/supprimer/', views.supprimer_installation, name='supprimer_installation'),

    # Diagnostics
    path('diagnostics/', views.liste_diagnostics, name='liste_diagnostics'),
    path('diagnostics/ajouter/', views.ajouter_diagnostic, name='ajouter_diagnostic'),
    path('diagnostics/<int:id>/modifier/', views.modifier_diagnostic, name='modifier_diagnostic'),
    path('diagnostics/<int:id>/supprimer/', views.supprimer_diagnostic, name='supprimer_diagnostic'),

    

    #Historique boitier
    path('boitiers/<int:id>/historique/', views.historique_boitier, name='historique_boitier'),

    # APIs pour l'ajout rapide
path('api/boitier/ajouter/', views.api_ajouter_boitier, name='api_ajouter_boitier'),
path('api/sim/ajouter/', views.api_ajouter_sim, name='api_ajouter_sim'),
path('api/vehicule/ajouter/', views.api_ajouter_vehicule, name='api_ajouter_vehicule'),
path('api/technicien/ajouter/', views.api_ajouter_technicien, name='api_ajouter_technicien'),
path('api/client/ajouter/', views.api_ajouter_client, name='api_ajouter_client'),
    
]
