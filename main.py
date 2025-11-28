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
VERSION = "1.0"
console = Console()

# Définition des fonctions
def fonctionnalites_avancees():
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
    choix = Prompt.ask("Choisissez une option", choices=["1", "2", "3"], default="3")
    if choix == '1':
        try:
            id_livre = int(Prompt.ask("Entrez l'ID du livre à noter"))
            noter_livre(livres, id_livre)
        except ValueError:
            console.print("[red]Erreur : L'ID du livre et la note doivent être des entiers.[/red]")
    elif choix == '2':
        export_csv(livres)
    elif choix == '3':
        return
    else:
        console.print("[red]Erreur : Option invalide, veuillez réessayer.[/red]")

# Programme principal
if __name__ == "__main__":
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
        
        choix = Prompt.ask("Choisissez une option", choices=[str(i) for i in range(1, 11)], default="2")
        
        if choix == '1':
            console.print(Panel.fit("[bold]Ajout d'un nouveau livre[/bold]", style="green"))
            titre = Prompt.ask("Titre")
            auteur = Prompt.ask("Auteur")
            genre = Prompt.ask("Genre")
            try:
                annee = int(Prompt.ask("Année de publication"))
            except ValueError:
                print("Erreur : L'année de publication doit être un entier.")
                continue
            try:
                prix = float(Prompt.ask("Prix"))
            except ValueError:
                print("Erreur : Le prix doit être un nombre.")
                continue
            ajouter_livre(livres, titre, auteur, genre, annee, prix)
        elif choix == '2':
            critere_tri = Prompt.ask("Critère de tri", choices=["ID", "titre", "auteur", "prix"], default="ID")
            afficher_tous_les_livres(livres, critere_tri)
        elif choix == '3':
            critere = Prompt.ask("Critère de recherche", choices=["titre", "auteur", "genre"], default="titre")
            valeur = Prompt.ask("Valeur à rechercher").strip()
            resultats = rechercher_livre(livres, critere, valeur)
            if resultats:
                afficher_tous_les_livres(resultats)
            else:
                console.print("[yellow]Aucun livre trouvé correspondant à la recherche.[/yellow]")
        elif choix == '4':
            try:
                id_livre = int(Prompt.ask("Entrez l'ID du livre à emprunter"))
            except ValueError:
                console.print("[red]Erreur : L'ID du livre doit être un entier.[/red]")
                continue
            emprunter_livre(livres, id_livre)
        elif choix == '5':
            try:
                id_livre = int(Prompt.ask("Entrez l'ID du livre à retourner"))
            except ValueError:
                console.print("[red]Erreur : L'ID du livre doit être un entier.[/red]")
                continue
            retourner_livre(livres, id_livre)
        elif choix == '6':
            genre = Prompt.ask("Entrez le genre à filtrer").strip()
            livres_genre = filtrer_par_genre(livres, genre)
            if livres_genre:
                afficher_tous_les_livres(livres_genre)
            else:
                console.print(f"[yellow]Aucun livre trouvé dans le genre '{genre}'.[/yellow]")
        elif choix == '7':
            generer_rapport(livres)
        elif choix == '8':
            try:
                id_livre = int(Prompt.ask("Entrez l'ID du livre à supprimer"))
            except ValueError:
                console.print("[red]Erreur : L'ID du livre doit être un entier.[/red]")
                continue
            supprimer_livre(livres, id_livre)
        elif choix == '9':
            fonctionnalites_avancees()
        elif choix == '10':
            console.print("Quitter le programme. Au revoir!")
            break
        else:
            console.print("[red]Erreur : Option invalide, veuillez réessayer.[/red]")
        
        sauvegarder_bibliotheque(livres)
    sauvegarder_bibliotheque(livres)
