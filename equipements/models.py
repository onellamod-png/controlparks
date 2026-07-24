# On importe le module models de Django pour créer nos tables
from django.db import models
# On importe le modèle User intégré de Django (non utilisé ici mais disponible)
from django.contrib.auth.models import User


# ============================================================
# RÉFÉRENTIEL - Tables gérées par l'administrateur
# ============================================================

class ModeleBoitier(models.Model):
    # Nom du modèle de boîtier (ex: Teltonika FMB920), unique = pas de doublon
    nom = models.CharField(max_length=100, unique=True)
    # Description optionnelle du modèle (peut être vide)
    description = models.TextField(blank=True)

    # Définit comment afficher un objet ModeleBoitier (ex: dans une liste déroulante)
    def __str__(self):
        return self.nom


class Operateur(models.Model):
    # Nom de l'opérateur téléphonique (ex: Togocom, Moov), unique = pas de doublon
    nom = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nom


class TypeDefaut(models.Model):
    # Libellé du type de défaut coché par le technicien (ex: "Pas de communication")
    libelle = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.libelle


# ============================================================
# UTILISATEURS
# ============================================================

class Technicien(models.Model):
    # Nom du technicien
    nom = models.CharField(max_length=100)
    # Prénom (blank=True = peut être vide dans le formulaire)
    prenom = models.CharField(max_length=100, blank=True)
    # Numéro de téléphone (CharField car pas de calcul sur un numéro)
    telephone = models.CharField(max_length=50, blank=True)
    # Adresse email
    email = models.CharField(max_length=150, blank=True)
    # Mot de passe (stocké de façon sécurisée)
    mot_de_passe = models.CharField(max_length=255, blank=True)
    # True = administrateur, False = technicien normal
    est_administrateur = models.BooleanField(default=False)

    # Affiche le nom complet du technicien
    def __str__(self):
        return f"{self.nom} {self.prenom}"


# ============================================================
# MATÉRIEL
# ============================================================

class Boitier(models.Model):
    # Liste des états possibles d'un boîtier (code, libellé affiché)
    ETAT_CHOICES = [
        ("stock", "En stock"),
        ("installe", "Installé"),
        ("panne", "En panne"),
        ("retire", "Retiré"),
    ]
    # Numéro de série unique du boîtier
    numero_serie = models.CharField(max_length=100, unique=True)
    # Lien vers le modèle du boîtier (clé étrangère)
    # on_delete=PROTECT = on ne peut pas supprimer un modèle utilisé par un boîtier
    modele = models.ForeignKey(ModeleBoitier, on_delete=models.PROTECT, related_name="boitiers")
    # Date d'achat (null=True = peut être vide en base, blank=True = peut être vide dans le formulaire)
    date_achat = models.DateField(null=True, blank=True)
    # État actuel du boîtier, par défaut "En stock"
    etat = models.CharField(max_length=20, choices=ETAT_CHOICES, default="stock")

    # Affiche le numéro de série et l'état lisible (ex: "BT-001 (En stock)")
    def __str__(self):
        return f"{self.numero_serie} ({self.get_etat_display()})"


class CarteSIM(models.Model):
    ETAT_CHOICES = [
        ("active", "Active"),
        ("suspendue", "Suspendue"),
        ("resiliee", "Résiliée"),
    ]
    # Numéro de téléphone - identifiant principal utilisé par les techniciens
    numero_telephone = models.CharField(max_length=30, unique=True)
    # ICCID - optionnel, numéro technique gravé sur la carte
    iccid = models.CharField(max_length=30, blank=True)
    # Opérateur téléphonique
    operateur = models.ForeignKey(Operateur, on_delete=models.PROTECT, related_name="cartes_sim")
    # État actuel de la SIM, par défaut "Active"
    etat = models.CharField(max_length=20, choices=ETAT_CHOICES, default="active")
    # Date d'activation (optionnelle)
    date_activation = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.numero_telephone} ({self.operateur})"
# ============================================================
# CLIENTS / VÉHICULES
# ============================================================

class Client(models.Model):
    nom = models.CharField(max_length=150)
    prenom = models.CharField(max_length=150, blank=True)
    telephone = models.CharField(max_length=50, blank=True)
    email = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return f"{self.nom} {self.prenom}"


class Vehicule(models.Model):
    # Plaque d'immatriculation unique du véhicule
    plaque = models.CharField(max_length=20, unique=True)
    marque = models.CharField(max_length=100, blank=True)
    modele = models.CharField(max_length=100, blank=True)
    # Lien vers le client propriétaire du véhicule
    # SET_NULL = si le client est supprimé, le véhicule reste mais sans client
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, related_name="vehicules")

    def __str__(self):
        return self.plaque


# ============================================================
# INSTALLATIONS - Table centrale de la traçabilité
# ============================================================

class Installation(models.Model):
    # Boîtier installé - lien vers la table Boitier
    boitier = models.ForeignKey(Boitier, on_delete=models.PROTECT, related_name="installations")
    # Carte SIM utilisée - lien vers la table CarteSIM
    carte_sim = models.ForeignKey(CarteSIM, on_delete=models.PROTECT, related_name="installations")
    # Véhicule concerné - lien vers la table Vehicule
    vehicule = models.ForeignKey(Vehicule, on_delete=models.PROTECT, related_name="installations")
    # Technicien qui a réalisé l'installation
    technicien = models.ForeignKey(Technicien, on_delete=models.PROTECT, related_name="installations")
    # Date à laquelle le boîtier a été installé
    date_installation = models.DateField()
    # Date de désinstallation - vide si l'installation est encore en cours
    date_desinstallation = models.DateField(null=True, blank=True)
    # Commentaire libre du technicien sur l'installation
    commentaire = models.TextField(blank=True)

    # Affiche le boîtier, le véhicule et le statut de l'installation
    def __str__(self):
        statut = "en cours" if self.date_desinstallation is None else "terminée"
        return f"{self.boitier} sur {self.vehicule} ({statut})"

    class Meta:
        # Trie les installations de la plus récente à la plus ancienne
        ordering = ["-date_installation"]


class Diagnostic(models.Model):
    # Origine du diagnostic : signalé sur le terrain ou découvert en atelier
    ORIGINE_CHOICES = [
        ("terrain", "Signalé sur le terrain"),
        ("atelier", "Découvert en atelier"),
    ]
    # Installation concernée par ce diagnostic
    installation = models.ForeignKey(Installation, on_delete=models.CASCADE, related_name="diagnostics")
    # Défauts constatés - relation N,N car un diagnostic peut avoir plusieurs défauts
    defauts = models.ManyToManyField(TypeDefaut, related_name="diagnostics")
    # Origine du problème (terrain ou atelier)
    origine = models.CharField(max_length=20, choices=ORIGINE_CHOICES, default="terrain")
    # Commentaire libre sur le diagnostic
    commentaire = models.TextField(blank=True)
    # Date et heure du signalement - remplie automatiquement à la création
    date_signalement = models.DateTimeField(auto_now_add=True)
    # Technicien qui a signalé le problème
    signale_par = models.ForeignKey(Technicien, on_delete=models.SET_NULL, null=True, related_name="diagnostics_signales")

    def __str__(self):
        return f"Diagnostic du {self.date_signalement:%d/%m/%Y} - {self.installation}"


# ============================================================
# JOURNAL - Traçabilité des modifications
# ============================================================

class JournalModification(models.Model):
    # Technicien qui a effectué la modification
    technicien = models.ForeignKey(Technicien, on_delete=models.SET_NULL, null=True)
    # Nom de la table modifiée (ex: "Boitier", "CarteSIM")
    modele_concerne = models.CharField(max_length=50)
    # Identifiant de l'objet modifié
    objet_id = models.PositiveIntegerField()
    # Description de la modification effectuée
    description = models.CharField(max_length=255)
    # Date et heure de la modification - remplie automatiquement
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.date:%d/%m/%Y %H:%M} - {self.technicien} - {self.modele_concerne}#{self.objet_id}"

    class Meta:
        # Trie les modifications de la plus récente à la plus ancienne
        ordering = ["-date"]