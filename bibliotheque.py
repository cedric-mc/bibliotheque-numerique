#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module : Bibliothèque Numérique - Fonctions
Description : Fonctions de gestion de la bibliothèque numérique.
Auteur : Cédric MARIYA CONSTANTINE
Date : 2025
"""

# Importation des modules nécessaires
import csv
import datetime
import json
import os
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.panel import Panel


# Définition des constantes
console = Console()

# Définition des fonctions
def ajouter_livre(livres, titre, auteur, genre, annee, prix):
    """Fonction pour ajouter un nouveau livre à la bibliothèque avec ID unique.
    
    Args:
        titre (str): Titre du livre.
        auteur (str): Auteur du livre.
        genre (str): Genre du livre.
        annee (int): Année de publication.
        prix (float): Prix du livre.
    """
    # Vérification des données manquantes
    donnees_manquantes = [nom for nom, val in {"titre": titre, "auteur": auteur, "genre": genre, "année de publication": annee, "prix": prix}.items() if not val]
    # Si des données sont manquantes, on affiche un message d'erreur clair
    if donnees_manquantes:
        console.print(f"[red]Erreur : Les données suivantes sont manquantes :[/red] {', '.join(donnees_manquantes)}")
        return
    
    # Vérification de la validité des données (année, prix positif, etc.)
    if not isinstance(annee, int) or annee < 1000 or annee > datetime.datetime.now().year:
        console.print("[red]Erreur : L'année de publication doit être un entier valide entre 0 et l'année actuelle.[/red]")
        return
    if not isinstance(prix, (int, float)) or prix < 0:
        console.print("[red]Erreur : Le prix doit être un nombre positif.[/red]")
        return
    
    # Ajout du livre avec un ID unique
    livre_id = len(livres) + 1
    livres.append({
        "id": livre_id,
        "titre": titre, 
        "auteur": auteur, 
        "genre": genre, 
        "année_publication": annee, 
        "prix": prix, 
        "disponible": True, # Livre disponible par défaut
        "notes": [] # Liste pour stocker les notes des utilisateurs
    })
    console.print(f"[green]Livre '{titre}' ajouté avec l'ID {livre_id}.[/green]")


def afficher_tous_les_livres(livres, critere_tri="ID"):
    """Fonction pour afficher tous les livres de la bibliothèque de manière lisible, triers par un critère spécifié (ID, titre, auteur, prix).

    Args:
        livres (list): Liste des livres à afficher.
        critere_tri (str): Critère de tri ("ID", "titre", "auteur", "prix").
    """
    # Vérification si la liste des livres est vide
    if not livres:
        console.print("[yellow]Aucun livre dans la bibliothèque.[/yellow]")
        return
    
    # Création du tableau avec Rich
    table = Table(title="📚 Liste des livres")
    table.add_column("ID", justify="center")
    table.add_column("Titre")
    table.add_column("Auteur")
    table.add_column("Genre", justify="center")
    table.add_column("Année", justify="center")
    table.add_column("Prix (€)", justify="center")
    table.add_column("Disponible", justify="center")
    table.add_column("Note", justify="center")

    # Couleurs alternées pour les lignes
    couleur_pairs = "on #2c2c2c"      # gris foncé
    couleur_impairs = "on #1f1f1f"    # encore plus foncé

    # Ajout des lignes au tableau
    livres_tries = sorted(livres, key=lambda x: x[critere_tri.lower()] if critere_tri.lower() in x else x["id"]) # Tri des livres selon le critère
    for index, livre in enumerate(livres_tries): # Parcours des livres triés avec index pour les couleurs
        dispo = "[green]✔[/]" if livre["disponible"] else "[red]✘[/]" # Indicateur de disponibilité
        if livre.get("notes"): # Calcul de la note moyenne si des notes existent
            note_moyenne = f"{sum(livre['notes']) / len(livre['notes']):.2f}/5 ⭐"
        else: # Pas de notes disponibles
            note_moyenne = "N/A"
        # Ajout de la ligne avec la couleur appropriée
        table.add_row(str(livre["id"]), livre["titre"], livre["auteur"], livre["genre"], str(livre["année_publication"]), f"{livre['prix']:.2f}", dispo, note_moyenne, style=couleur_pairs if index % 2 == 0 else couleur_impairs)
    console.print(table) # Affichage du tableau
    console.print(f"[blue]Trié par : {critere_tri}[/blue]") # Affichage du critère de tri


def rechercher_livre(livres, critere, valeur):
    """Fonction pour rechercher par titre, auteur ou genre (case-insensitive).

    Args:
        livres (list): Liste des livres à rechercher.
        critere (str): Critère de recherche ("titre", "auteur", "genre").
        valeur (str): Valeur à rechercher.
    Returns:
        list: Liste des livres correspondant au critère et à la valeur.
    """
    # Normalisation du critère et de la valeur pour la recherche insensible à la casse
    champ = critere.strip().lower()
    if champ not in {"titre", "auteur", "genre"}: # Vérification du critère valide
        console.print("[red]Erreur : Critère de recherche invalide. Utilisez 'titre', 'auteur' ou 'genre'.[/red]")
        return []
    target = valeur.strip().casefold() # Valeur cible en minuscules pour comparaison
    # Recherche des livres correspondant au critère et à la valeur
    try:
        resultats = [livre for livre in livres if target in str(livre.get(champ, "")).casefold()]
    except KeyError: # Gestion d'erreur si le critère n'existe pas dans les données des livres
        console.print(f"[red]Erreur : Le critère '{critere}' n'existe pas dans les données des livres.[/red]")
        return []
    return resultats


def supprimer_livre(livres, id_livre):
    """Fonction pour supprimer un livre après confirmation.

    Args:
        livres (list): Liste des livres.
        id_livre (int): ID du livre à supprimer.
    """
    # Recherche du livre par ID
    for i, livre in enumerate(livres):
        if livre["id"] == id_livre: # Livre trouvé
            # Demander confirmation avant suppression
            confirmation = Prompt.ask(f"Confirmez-vous la suppression du livre '{livre['titre']}' (ID {id_livre}) ?", choices=["Oui", "Non"], default="Non")
            if confirmation.lower() == 'oui': # Suppression confirmée
                del livres[i] # Suppression du livre de la liste
                console.print(f"[green]Livre ID {id_livre} supprimé.[/green]")
            else: # Suppression annulée
                console.print("[yellow]Suppression annulée.[/yellow]")
            return
    console.print(f"[red]Erreur : Livre avec ID {id_livre} non trouvé.[/red]")
    return


def emprunter_livre(livres, id_livre):
    """Fonction pour emprunter un livre si disponible, change le statut à "emprunté" avec validation.

    Args:
        livres (list): Liste des livres.
        id_livre (int): ID du livre à emprunter.
    """
    # Recherche du livre par ID
    for livre in livres:
        if livre["id"] == id_livre: # Livre trouvé
            if livre["disponible"]: # Vérification de la disponibilité
                # Demander confirmation avant emprunt
                confirmation = Prompt.ask(f"Confirmez-vous l'emprunt du livre '{livre['titre']}' (ID {id_livre}) ?", choices=["Oui", "Non"], default="Non")
                if confirmation.lower() == 'oui': # Emprunt confirmé
                    livre["disponible"] = False # Changement du statut à emprunté
                    console.print(f"[green]Livre ID {id_livre} emprunté avec succès.[/green]")
                else: # Emprunt annulé
                    console.print("[yellow]Emprunt annulé.[/yellow]")
            else: # Livre non disponible
                console.print(f"[red]Erreur : Le livre '{livre['titre']}' (ID {id_livre}) n'est pas disponible pour l'emprunt.[/red]")
            return
    console.print(f"[red]Erreur : Livre avec ID {id_livre} non trouvé.[/red]")


def retourner_livre(livres, id_livre):
    """Fonction pour retourner un livre emprunté, change le statut à "disponible" avec validation.

    Args:
        livres (list): Liste des livres.
        id_livre (int): ID du livre à retourner.
    """
    for livre in livres: # Recherche du livre par ID
        if livre["id"] == id_livre: # Livre trouvé
            if not livre["disponible"]: # Vérification si le livre est emprunté
                # Demander confirmation avant retour
                confirmation = Prompt.ask(f"Confirmez-vous le retour du livre '{livre['titre']}' (ID {id_livre}) ?", choices=["Oui", "Non"], default="Non")
                if confirmation.lower() == 'oui': # Retour confirmé
                    livre["disponible"] = True # Changement du statut à disponible
                    noter_livre(livres, id_livre) # Appel de la fonction pour noter le livre après retour
                    console.print(f"[green]Livre ID {id_livre} retourné avec succès.[/green]")
                else: # Retour annulé
                    console.print("[yellow]Retour annulé.[/yellow]")
            else: # Livre déjà disponible
                console.print(f"[red]Erreur : Le livre '{livre['titre']}' (ID {id_livre}) n'était pas emprunté.[/red]")
            return
    console.print(f"[red]Erreur : Livre avec ID {id_livre} non trouvé.[/red]")


def filtrer_par_genre(livres, genre):
    """Fonction pour filtrer les livres par un genre spécifique.

    Args:
        livres (list): Liste des livres.
        genre (str): Genre à filtrer.
    Returns:
        list: Liste des livres du genre spécifié.
    """
    # Normalisation du genre pour la comparaison insensible à la casse
    genre_cible = genre.strip().casefold()
    livres_filtres = [livre for livre in livres if livre["genre"].casefold() == genre_cible] # Filtrage des livres par genre
    return livres_filtres


def noter_livre(livres, id_livre):
    """Fonction pour noter un livre sur une échelle de 1 à 5.

    Args:
        livres (list): Liste des livres.
        id_livre (int): ID du livre à noter.
        note (int): Note à attribuer (1 à 5).
    """
    console.print(Panel.fit(f"[bold]Notation du livre ID {id_livre}[/bold]", style="green"))
    console.print("Qu'avez-vous pensé de ce livre ?")
    note = int(Prompt.ask("Entrez la note (1 à 5)")) # Note à attribuer
    if note < 1 or note > 5: # Vérification de la validité de la note
        console.print("[red]Erreur : La note doit être entre 1 et 5.[/red]")
        return
    for livre in livres: # Recherche du livre par ID
        if livre["id"] == id_livre: # Livre trouvé
            livre.setdefault("notes", []).append(note) # Ajout de la note à la liste des notes
            note_emoji = "⭐" * note # Représentation visuelle de la note
            console.print(f"[green]Livre ID {id_livre} noté {note}/5 {note_emoji}.[/green]")
            return
    console.print(f"[red]Erreur : Livre avec ID {id_livre} non trouvé.[/red]")


def generer_rapport(livres):
    """Fonction pour afficher des statistiques sur la bibliothèque : nombre total, disponibles, empruntés, prix total, genre le plus représenté, livres les plus/moins chers.

    Args:
        livres (list): Liste des livres.
    """
    # Calcul des statistiques de base
    total_livres = len(livres)
    livres_disponibles = sum(1 for livre in livres if livre["disponible"])
    livres_empruntes = total_livres - livres_disponibles  # Calcul des livres empruntés
    prix_total = sum(livre["prix"] for livre in livres) # Somme des prix de tous les livres
    
    # Calcul du genre le plus représenté
    genres_count = {}
    for livre in livres: # Comptage des genres
        genre = livre["genre"] # Récupération du genre du livre
        genres_count[genre] = genres_count.get(genre, 0) + 1 # Incrémentation du compteur pour le genre
    genre_plus_represente = max(genres_count, key=genres_count.get) if genres_count else "N/A" # Genre avec le maximum de livres
    
    # Livres les plus chers et les moins chers
    if livres: # Vérification si la liste des livres n'est pas vide
        livre_plus_cher = max(livres, key=lambda x: x["prix"]) # Livre avec le prix maximum
        livre_moins_cher = min(livres, key=lambda x: x["prix"]) # Livre avec le prix minimum
    else: # Liste vide
        livre_plus_cher = livre_moins_cher = {"titre": "N/A", "prix": 0}

    # Livre le plus apprécié
    livres_avec_notes = [livre for livre in livres if livre.get("notes")]
    if livres_avec_notes: # Vérification si des livres ont des notes
        livre_plus_apprecie = max(livres_avec_notes, key=lambda x: sum(x["notes"]) / len(x["notes"])) # Livre avec la note moyenne la plus élevée
        note_moyenne = sum(livre_plus_apprecie["notes"]) / len(livre_plus_apprecie["notes"]) # Calcul de la note moyenne
    else: # Aucun livre n'a de notes
        livre_plus_apprecie = {"titre": "N/A"}
        note_moyenne = 0
    
    # Livre le moins apprécié
    if livres_avec_notes: # Vérification si des livres ont des notes
        livre_moins_apprecie = min(livres_avec_notes, key=lambda x: sum(x["notes"]) / len(x["notes"])) # Livre avec la note moyenne la plus basse
        note_moyenne_moins = sum(livre_moins_apprecie["notes"]) / len(livre_moins_apprecie["notes"]) # Calcul de la note moyenne
    else: # Aucun livre n'a de notes
        livre_moins_apprecie = {"titre": "N/A"}
        note_moyenne_moins = 0
    
    # Affichage du rapport
    console.print(Panel.fit(f"[bold]📊 Rapport de la Bibliothèque Numérique[/bold]", style="cyan"))
    console.print(f"Nombre total de livres : [bold]{total_livres}[/bold]")
    console.print(f"Livres disponibles : [bold]{livres_disponibles}[/bold]")
    console.print(f"Livres empruntés : [bold]{livres_empruntes}[/bold]")
    console.print(f"Prix total des livres : [bold]{prix_total:.2f} €[/bold]")
    console.print(f"Genre le plus représenté : [bold]{genre_plus_represente}[/bold]")
    console.print(f"Livre le plus cher : [bold underline]{livre_plus_cher['titre']}[/underline bold] à [bold]{livre_plus_cher['prix']:.2f} €[/bold]")
    console.print(f"Livre le moins cher : [bold underline]{livre_moins_cher['titre']}[/underline bold] à [bold]{livre_moins_cher['prix']:.2f} €[/bold]")
    console.print(f"Livre le plus apprécié : [bold underline]{livre_plus_apprecie['titre']}[/underline bold] avec une note moyenne de [bold]{note_moyenne:.2f}/5 ⭐[/bold]")
    console.print(f"Livre le moins apprécié : [bold underline]{livre_moins_apprecie['titre']}[/underline bold] avec une note moyenne de [bold]{note_moyenne_moins:.2f}/5 ⭐[/bold]")


def charger_bibliotheque():
    """Fonction pour charger les livres depuis `bibliotheque.json`.

    Returns:
        list: Liste des livres chargés.
    """
    # Vérification de l'existence du fichier
    if os.path.exists("bibliotheque.json"):
        try: # Chargement des données depuis le fichier JSON
            with open("bibliotheque.json", "r", encoding="utf-8") as f:
                livres = json.load(f)
            console.print("[green]Bibliothèque chargée depuis 'bibliotheque.json'.[/green]")
            return livres
        except json.JSONDecodeError: # Gestion d'erreur si le fichier JSON est corrompu ou mal formaté
            console.print("[red]Erreur : Le fichier 'bibliotheque.json' est corrompu ou mal formaté.[/red]")
            return []
    else: # Fichier non trouvé, initialisation d'une bibliothèque vide
        console.print("[yellow]Aucun fichier 'bibliotheque.json' trouvé. Bibliothèque vide initialisée.[/yellow]")
        return []


def sauvegarder_bibliotheque(livres):
    """Fonction pour sauvegarder les livres dans `bibliotheque.json`.

    Args:
        livres (list): Liste des livres à sauvegarder.
    """
    try: # Sauvegarde des données dans le fichier JSON
        with open("bibliotheque.json", "w", encoding="utf-8") as f:
            json.dump(livres, f, ensure_ascii=False, indent=4)
        console.print("[green]Bibliothèque sauvegardée dans 'bibliotheque.json'.[/green]")
    except IOError: # Gestion d'erreur si le fichier ne peut pas être écrit
        console.print("[red]Erreur : Impossible de sauvegarder dans 'bibliotheque.json'.[/red]")


def export_csv(livres):
    """Fonction pour exporter la bibliothèque au format CSV.

    Args:
        livres (list): Liste des livres à exporter.
    """
    try: # Exportation des données dans un fichier CSV
        with open('bibliotheque.csv', "w", newline='', encoding="utf-8") as csvfile:
            # Définition des en-têtes du CSV
            fieldnames = ["id", "titre", "auteur", "genre", "année_publication", "prix", "disponible"]
            # Création de l'écrivain CSV avec les en-têtes définis
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader() # Écriture de l'en-tête dans le fichier CSV
            # Écriture des données des livres dans le fichier CSV
            for livre in livres:
                writer.writerow({
                    "id": livre["id"],
                    "titre": livre["titre"],
                    "auteur": livre["auteur"],
                    "genre": livre["genre"],
                    "année_publication": livre["année_publication"],
                    "prix": livre["prix"],
                    "disponible": livre["disponible"]
                })
        console.print(f"[green]Bibliothèque exportée avec succès dans 'bibliotheque.csv'.[/green]")
    except IOError: # Gestion d'erreur si le fichier ne peut pas être écrit
        console.print(f"[red]Erreur : Impossible d'exporter dans 'bibliotheque.csv'.[/red]")