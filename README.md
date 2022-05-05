## Sommaire:
- Application d'organisateur de tournois d'échecs.
- Générer un nouveau fichier flake8-html.

# Application d'organisateur de tournois d'échecs

Cette application permet de créer des tournois entre plusieurs joueurs et de générer des rapports.
#

# Notice d'utilisation:
Pour démarrer le programme il suffit d'éxcécuter le fichier main.py du code d'application.

Une fois le programme lancé, vous aurez accès à différents menus. Voici une descriptions des différents menus:
#

## Sommaire:
- Menu principal
  - Menu Tournoi
     - Liste des tournois
        - Menu du tournoi selectionné
           - Démarrer le tournoi
           - Joueurs
           - Tours
           - Matchs
           - Description
     - Ajouter un tournoi
  - Menu Joueurs
    - Liste des joueurs
    - Ajouter un joueur
  - Menu Sauvegarder
  - Menu Charger
#
## Menu principal
```
--------------
MENU PRINCIPAL
--------------
1 -- Tournois
2 -- Joueurs
3 -- Sauvegarder
4 -- Charger
5 -- Quitter
```
- 1 -- Permet de voir la liste des tournois, d'en ajouter, et de les jouer.
- 2 -- Permet de voir la liste des joueurs et d'en ajouter.
- 3 -- Permet de sauvegarder vos données.
- 4 -- Permet de charger vos données.
- 5 -- Selectionnez ce choix si vous souhaitez quitter l'application
  
## 1. Menu Tournoi
```
------------
MENU TOURNOI
------------
1 -- Liste des tournois
2 -- Nouveau tournoi
3 -- Retour
```
- 1 -- Permet de voir la liste des tournois et d'en selectionner un.
- 2 -- Permet de créer un nouveau tournoi
- 3 -- Permet de retourner au menu principal

### 1.1 Liste des tournois
```
-------------------------------------------------------------------
LISTE DES TOURNOIS: Veuillez selectionner un tournoi pour commencer
-------------------------------------------------------------------
1 -- Tournoi 1
2 -- Tournoi 2
3 -- Tournoi 3
...
n -- Retour
```
Pour selectionner un tournoi créé, il suffit d'entrer le choix qui correspond pour accéder au tournoi voulu.

Pour revenir au menu des tournois choissiez **Retour**.

### 1.1.1 Menu du tournoi selectionné
```
------------------
MENU DU TOURNOI: *Tournoi selectionné*
------------------
1 -- Démarrer le tournoi
2 -- Joueurs
3 -- Tours
4 -- Matchs
5 -- Description
6 -- Retour
```
- 1 -- Permet de démarrer le tournoi:
  - Les tours vont être joué un à un et l'utilisateur pourra entrer les résultats des matchs à la fin de chaque tours.
- 2 -- Permet de voir les joueurs attribué au tournoi.
- 3 -- Permet de voir le rapport des tours joué du tournoi selectionné.
- 4 -- Permet de voir le rapport des matchs joué du tournoi selectionné.
- 5 -- Permet de saisir ou de modifier la description du tournoi selectionné.
- 6 -- Permet de revenir à la liste des tournois.

### 1.2 Ajouter un tournoi
Lors ce que vous voulez ajouter un tournoi, plusieurs informations vous seront demandées:
```
NOUVEAU TOURNOI
---------------
Nom du tournoi:
Lieu du tournoi: 
Date du tournoi: 
règle du tournoi ? (bullet, blitz ou speed) 
Nombre de tours:
```
- Nom du tournoi : Entrez le nom du tournoi
- Lieu du tournoi : Entrez le lieu du tournoi
- Date du tournoi : Saisissez la date du tournoi au format xx/xx/xx
- Règle du tournoi ? (bullet, blitz ou speed): Saisissez la règle du tournoi
- Nombre de tours: Entrez le nombre de tour pour ce tournoi. Vous devez au minimum mettre 1.

*à finir...*

# Générer un nouveau fichier flake8-html

*à venir...*