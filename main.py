#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module : Bibliothèque Numérique - Menu
Description : Programme principal pour gérer la bibliothèque numérique.
Auteur : Cédric MARIYA CONSTANTINE
Date : 2025
"""

# Importation des modules nécessaires
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.align import Align
from bibliotheque import ajouter_livre, afficher_tous_les_livres, rechercher_livre, emprunter_livre, retourner_livre, filtrer_par_genre, generer_rapport, supprimer_livre, charger_bibliotheque, sauvegarder_bibliotheque, noter_livre, export_csv

# Définition des constantes
VERSION = "1.2"
console = Console()

# Définition des fonctions
def fonctionnalites_avancees():
    """Fonction pour gérer les fonctionnalités avancées de la bibliothèque numérique."""
    # Afficher le menu des fonctionnalités avancées
    menu_panel = Panel.fit(
        "\n".join([
            "[bold]======= FONCTIONNALITÉS AVANCÉES ========[/bold]",
            "[cyan]1[/cyan]. Noter un livre (1 à 5 étoiles)",
            "[cyan]2[/cyan]. Exporter la bibliothèque au format CSV",
            "[cyan]3[/cyan]. Retour au menu principal"
        ]),
        title="Menu",
        subtitle="Entrez le numéro de l'option",
        style="magenta"
    )
    console.print(menu_panel)
    # Gérer le choix de l'utilisateur
    choix = Prompt.ask("Choisissez une option", choices=["1", "2", "3"], default="3")
    if choix == '1': # Noter un livre
        try:
            id_livre = int(Prompt.ask("Entrez l'ID du livre à noter"))
            noter_livre(livres, id_livre)
        except ValueError:
            console.print("[red]Erreur : L'ID du livre et la note doivent être des entiers.[/red]")
    elif choix == '2': # Exporter au format CSV
        export_csv(livres)
    elif choix == '3': # Retour au menu principal
        return
    else: # Option invalide
        console.print("[red]Erreur : Option invalide, veuillez réessayer.[/red]")

# Programme principal
if __name__ == "__main__":
    # Affichage du titre
    console.print(Panel(Align.center(f"[bold]Bibliothèque Numérique — Version {VERSION}[/bold]", vertical="middle"), title="Bienvenue", subtitle="Cédric MARIYA CONSTANTINE", style="cyan"))
    # Initialisation de la bibliothèque
    livres = charger_bibliotheque()

    # Boucle principale du menu
    while True:
        # Afficher menu
        menu_panel = Panel.fit(
            "\n".join([
                "[bold]=== GESTION DE BIBLIOTHÈQUE ===[/bold]",
                "[cyan]1[/cyan]. Ajouter un livre",
                "[cyan]2[/cyan]. Afficher tous les livres",
                "[cyan]3[/cyan]. Rechercher un livre",
                "[cyan]4[/cyan]. Emprunter un livre",
                "[cyan]5[/cyan]. Retourner un livre",
                "[cyan]6[/cyan]. Filtrer par genre",
                "[cyan]7[/cyan]. Afficher les statistiques",
                "[cyan]8[/cyan]. Supprimer un livre",
                "[cyan]9[/cyan]. Fonctionnalités avancées",
                "[cyan]10[/cyan]. Quitter"
            ]),
            title="Menu",
            subtitle="Entrez le numéro de l'option",
            style="magenta"
        )
        console.print(menu_panel)
        
        # Gérer le choix de l'utilisateur
        choix = Prompt.ask("Choisissez une option", choices=[str(i) for i in range(1, 11)], default="2")
        if choix == '1': # Ajouter un livre
            console.print(Panel.fit("[bold]Ajout d'un nouveau livre[/bold]", style="green"))
            titre = Prompt.ask("Titre") # Titre du livre
            auteur = Prompt.ask("Auteur") # Auteur du livre
            genre = Prompt.ask("Genre") # Genre du livre
            # Validation de l'année et du prix
            try:
                annee = int(Prompt.ask("Année de publication"))
            except ValueError:
                console.print("[red]Erreur : L'année de publication doit être un entier.[/red]")
                continue
            try:
                prix = float(Prompt.ask("Prix"))
            except ValueError:
                console.print("[red]Erreur : Le prix doit être un nombre.[/red]")
                continue
            ajouter_livre(livres, titre, auteur, genre, annee, prix) # Appel de la fonction pour ajouter le livre

        elif choix == '2': # Afficher tous les livres
            # Demander le critère de tri
            critere_tri = Prompt.ask("Critère de tri", choices=["ID", "titre", "auteur", "prix"], default="ID")
            afficher_tous_les_livres(livres, critere_tri) # Appel de la fonction pour afficher les livres

        elif choix == '3': # Rechercher un livre
            # Demander le critère et la valeur de recherche
            critere = Prompt.ask("Critère de recherche", choices=["titre", "auteur", "genre"], default="titre")
            valeur = Prompt.ask("Valeur à rechercher").strip()
            resultats = rechercher_livre(livres, critere, valeur) # Appel de la fonction pour rechercher les livres
            if resultats: # Afficher les résultats si trouvés
                afficher_tous_les_livres(resultats)
            else:
                # Afficher un message si aucun livre n'est trouvé
                console.print("[yellow]Aucun livre trouvé correspondant à la recherche.[/yellow]")
                
        elif choix == '4': # Emprunter un livre
            try:
                id_livre = int(Prompt.ask("Entrez l'ID du livre à emprunter")) # ID du livre à emprunter
            except ValueError: # Gestion d'erreur si l'ID n'est pas un entier
                console.print("[red]Erreur : L'ID du livre doit être un entier.[/red]")
                continue
            emprunter_livre(livres, id_livre) # Appel de la fonction pour emprunter le livre

        elif choix == '5': # Retourner un livre
            try:
                id_livre = int(Prompt.ask("Entrez l'ID du livre à retourner")) # ID du livre à retourner
            except ValueError: # Gestion d'erreur si l'ID n'est pas un entier
                console.print("[red]Erreur : L'ID du livre doit être un entier.[/red]")
                continue
            retourner_livre(livres, id_livre) # Appel de la fonction pour retourner le livre
            
        elif choix == '6': # Filtrer par genre
            genre = Prompt.ask("Entrez le genre à filtrer").strip() # Genre à filtrer
            livres_genre = filtrer_par_genre(livres, genre) # Appel de la fonction pour filtrer par genre
            if livres_genre: # Afficher les livres si trouvés
                afficher_tous_les_livres(livres_genre)
            else: # Afficher un message si aucun livre n'est trouvé
                console.print(f"[yellow]Aucun livre trouvé dans le genre '{genre}'.[/yellow]")

        elif choix == '7': # Générer un rapport
            generer_rapport(livres) # Appel de la fonction pour générer le rapport

        elif choix == '8': # Supprimer un livre
            try:
                id_livre = int(Prompt.ask("Entrez l'ID du livre à supprimer")) # ID du livre à supprimer
            except ValueError: # Gestion d'erreur si l'ID n'est pas un entier
                console.print("[red]Erreur : L'ID du livre doit être un entier.[/red]")
                continue
            supprimer_livre(livres, id_livre) # Appel de la fonction pour supprimer le livre

        elif choix == '9': # Fonctionnalités avancées
            fonctionnalites_avancees() # Appel de la fonction pour les fonctionnalités avancées

        elif choix == '10': # Quitter
            console.print("Quitter le programme. Au revoir!") # Message de sortie
            break

        else: # Option invalide
            console.print("[red]Erreur : Option invalide, veuillez réessayer.[/red]")
        
        sauvegarder_bibliotheque(livres) # Sauvegarder la bibliothèque après chaque opération
    sauvegarder_bibliotheque(livres) # Sauvegarder la bibliothèque à la fin du programme