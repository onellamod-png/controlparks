from django.contrib import admin
from .models import (
    Boitier, CarteSIM, Client, Vehicule,
    Technicien, Installation, Diagnostic,
    TypeDefaut, ModeleBoitier, Operateur,
    JournalModification
)

admin.site.register(Boitier)
admin.site.register(CarteSIM)
admin.site.register(Client)
admin.site.register(Vehicule)
admin.site.register(Technicien)
admin.site.register(Installation)
admin.site.register(Diagnostic)
admin.site.register(TypeDefaut)
admin.site.register(ModeleBoitier)
admin.site.register(Operateur)
admin.site.register(JournalModification)