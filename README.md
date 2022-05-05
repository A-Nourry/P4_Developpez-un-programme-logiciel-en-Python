## Sommaire:
- Application d'organisateur de tournois d'échecs.
- Générer un nouveau fichier flake8-html.

# Application d'organisateur de tournois d'échecs

Cette application permet de créer des tournois entre plusieurs joueurs et de générer des rapports.

## Comment organiser un tournoi ?
- Avant de commencer, vous devez charger ou créer une liste de joueurs (8 joueurs minimum).
- Ensuite vous devez créer un tournoi, choisir le nombre de tours, puis attribuer 8 joueurs à celui-ci.
- Une fois le tournoi créé et sélectionné, vous aller pouvoir démarrer le tournoi ce qui exécutera un nombre de tours préalablement défini.
- À chaque tours, le programme générera des paires de joueurs suivant leur classement. Ensuite, à la fin de chaque tour, vous pourrez entrer les résultats de chaque match.

Une fois le tournoi terminé, vous aurez la possibilité d'afficher les différents rapports du tournoi, de le rejouer, d'en créer un nouveau ou d'en sélectionner un autre.

Pour plus de précisions, veuillez vous référer à la notice d'utilisation qui suit.

#

# Notice d'utilisation :
Pour démarrer le programme il suffit d'exécuter le fichier main.py du code d'application.

Une fois le programme lancé, vous aurez accès à différents menus. Voici une description de chacun de ceux-là :
#

## Sommaire:
- Menu principal
  - Menu Tournoi
     - Nouveau tournoi
     - Liste des tournois
        - Menu du tournoi sélectionné
           - Démarrer le tournoi
           - Joueurs
           - Tours
           - Matchs
           - Description
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
- 5 -- Sélectionnez ce choix si vous souhaitez quitter l'application
  
## 1. Menu Tournoi
```
------------
MENU TOURNOI
------------
1 -- Liste des tournois
2 -- Nouveau tournoi
3 -- Retour
```
- 1 -- Permet de voir la liste des tournois et d'en sélectionner un.
- 2 -- Permet de créer un nouveau tournoi
- 3 -- Permet de retourner au menu principal

### 1.1 Liste des tournois
```
---------------------------------------------------------------------
LISTE DES TOURNOIS : veuillez sélectionner un tournoi pour commencer.
---------------------------------------------------------------------
1 -- Tournoi 1
2 -- Tournoi 2
3 -- Tournoi 3
...
n -- Retour
```
Pour sélectionner un tournoi créé, il suffit d'entrer le choix qui correspond pour accéder au tournoi voulu.

Pour revenir au menu des tournois choisissez **Retour**.

### 1.1.1 Menu du tournoi selectionné
```
---------------------------------------
MENU DU TOURNOI : *Tournoi sélectionné*
---------------------------------------
1 -- Démarrer le tournoi
2 -- Joueurs
3 -- Tours
4 -- Matchs
5 -- Description
6 -- Retour
```
- 1 -- Permet de démarrer le tournoi :
  - Les tours vont être joués un à un et l'utilisateur pourra entrer les résultats des matchs à la fin de chaque tour.
- 2 -- Permet de voir les joueurs attribués au tournoi.
- 3 -- Permet de voir le rapport des tours joué du tournoi sélectionné.
- 4 -- Permet de voir le rapport des matchs joué du tournoi sélectionné.
- 5 -- Permet de saisir ou de modifier la description du tournoi sélectionné.
- 6 -- Permet de revenir à la liste des tournois.

### 1.2 Nouveau tournoi
Lorsque vous souhaitez créer un nouveau tournoi, plusieurs informations vous seront demandées :
```
NOUVEAU TOURNOI
---------------
Nom du tournoi:
Lieu du tournoi: 
Date du tournoi: 
règle du tournoi ? (bullet, blitz ou speed) 
Nombre de tours:
```
- Nom du tournoi : entrez le nom du tournoi
- Lieu du tournoi : entrez le lieu du tournoi
- Date du tournoi : saisissez la date du tournoi au format xx/xx/xx
- Règle du tournoi ? (bullet, blitz ou speed): saisissez la règle du tournoi.
- Nombre de tours : entrez le nombre de tours pour ce tournoi. Vous devez au minimum mettre 1.

*à finir...*

# Générer un nouveau fichier flake8-html

*à venir...*