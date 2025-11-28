# Bibliothèque Numérique 📚

## Description

**Bibliothèque Numérique** est une application Python permettant de gérer une bibliothèque pour une petite librairie ou un usage personnel.
Chaque livre est représenté par un dictionnaire contenant les informations suivantes :

| Champ               | Type      | Description                                  |
| ------------------- | --------- | -------------------------------------------- |
| `id`                | int       | Identifiant unique du livre                  |
| `titre`             | str       | Titre du livre                               |
| `auteur`            | str       | Nom de l'auteur                              |
| `genre`             | str       | Genre du livre                               |
| `année_publication` | int       | Année de publication                         |
| `prix`              | float     | Prix du livre en euros                       |
| `disponible`        | bool      | True si le livre est disponible, False sinon |
| `notes`             | list[int] | Notes attribuées au livre (1 à 5)            |

Les livres sont stockés dans le fichier **`bibliotheque.json`**, garantissant la persistance des données entre les exécutions.
L’application offre une interface **terminal colorée et conviviale** grâce à la bibliothèque `rich`.

---

## Fonctionnalités principales

* ✅ Ajouter un livre avec validation des données (titre, auteur, année, prix, genre)
* 📄 Afficher tous les livres de manière lisible et triable par ID, titre, auteur ou prix
* 🔍 Rechercher un livre par titre, auteur ou genre (recherche insensible à la casse)
* ❌ Supprimer un livre après confirmation
* 📚 Emprunter un livre si disponible
* 🔄 Retourner un livre emprunté
* 🎨 Filtrer les livres par genre
* 📊 Générer un rapport complet :

  * Nombre total de livres
  * Livres disponibles et empruntés
  * Prix total de la bibliothèque
  * Genre le plus représenté
  * Livre le plus cher / le moins cher
  * Livre le plus apprécié / le moins apprécié
* 💾 Charger et sauvegarder automatiquement la bibliothèque depuis/vers `bibliotheque.json`
* ⭐ Noter un livre (1 à 5 étoiles)
* 📁 Exporter la bibliothèque au format CSV

---

## Installation

### Prérequis

* Python 3.6 ou supérieur
* `pip` (gestionnaire de paquets Python)

**Optionnel mais recommandé :** créer un environnement virtuel pour isoler les dépendances.

### Étapes d’installation

1. **Cloner le dépôt GitHub :**

   ```bash
   git clone https://github.com/cedric-mc/bibliotheque-numerique.git
   cd bibliotheque-numerique
   ```
2. **(Optionnel) Créer et activer un environnement virtuel :**

   ```bash
   python -m venv env
   source env/bin/activate  # Sur Windows : `env\Scripts\activate`
   ```
3. **Installer les dépendances :**

   ```bash
   pip install -r requirements.txt
   ```
4. **Lancer l’application :**

   ```bash
   python main.py
   ```

---

## Utilisation

Une fois l’application lancée, un **menu interactif** s’affiche dans le terminal :

```
=== GESTION DE BIBLIOTHÈQUE ===
1. Ajouter un livre
2. Afficher tous les livres
3. Rechercher un livre
4. Emprunter un livre
5. Retourner un livre
6. Filtrer par genre
7. Afficher les statistiques
8. Supprimer un livre
9. Fonctionnalités avancées
10. Quitter
```

### Notes importantes

* Toutes les actions de modification (ajout, suppression, emprunt, retour, notation) **sauvegardent automatiquement** la bibliothèque.
* Les livres empruntés ne peuvent pas être empruntés à nouveau avant d’être retournés.
* La **notation** est facultative lors du retour d’un livre.
* L’export CSV permet de récupérer vos données sous un format facilement lisible dans Excel ou Google Sheets.

---

## Exemples d’utilisation

1. **Ajouter un livre :**

   * Choisir l’option `1` dans le menu.
   * Renseigner le titre, l’auteur, le genre, l’année de publication et le prix.
   * Le livre est ajouté avec un ID unique.

2. **Afficher tous les livres :**

   * Choisir l’option `2`.
   * Sélectionner le critère de tri (ID, titre, auteur, prix).

3. **Emprunter un livre :**

   * Choisir l’option `4`.
   * Entrer l’ID du livre.
   * Confirmer l’emprunt.

4. **Retourner un livre et noter :**

   * Choisir l’option `5`.
   * Entrer l’ID du livre.
   * Noter le livre (1 à 5 étoiles).

5. **Exporter la bibliothèque :**

   * Choisir l’option `9` > `2` (export CSV).
   * Le fichier `bibliotheque.csv` est créé dans le dossier courant.

---

## Conseils et bonnes pratiques

* Testez l’application avec **10 à 15 livres** pour profiter des statistiques et filtres.
* Validez toujours vos entrées pour éviter les erreurs (année correcte, prix positif, champs non vides).
* Utilisez un environnement virtuel pour éviter les conflits de dépendances.
* Le fichier JSON est auto-créé si inexistant.

---

## Dépendances

* `rich` : pour l’affichage en couleur et les tableaux
* Modules standard : `json`, `os`, `csv`, `datetime`

Installation via pip :

```bash
pip install rich
```

---

## Auteur

Cédric MARIYA CONSTANTINE — 2025
