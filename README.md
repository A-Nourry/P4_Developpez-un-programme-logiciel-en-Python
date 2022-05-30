## Sommaire:
- [Application d'organisateur de tournois d'échecs](#application-dorganisateur-de-tournois-déchecs)
  - [Comment organiser un tournoi ?](#comment-organiser-un-tournoi-)
- [Notice d'utilisation :](#notice-dutilisation-)
- [Description des différents menus:](#description-des-différents-menus)
  - [Menu principal](#menu-principal)
  - [1. Menu Tournoi](#1-menu-tournoi)
    - [1.1 Liste des tournois](#11-liste-des-tournois)
      - [1.1.1 Menu du tournoi selectionné](#111-menu-du-tournoi-selectionné)
        - [Joueurs](#joueurs)
    - [1.2 Nouveau tournoi](#12-nouveau-tournoi)
  - [2. Menu Joueurs](#2-menu-joueurs)
- [Générer un nouveau fichier flake8-html](#générer-un-nouveau-fichier-flake8-html)

# Application d'organisateur de tournois d'échecs

Cette application permet de créer des tournois entre plusieurs joueurs et de générer des rapports.

## Comment organiser un tournoi ?
- Avant de commencer, vous devez charger ou créer une liste de joueurs (8 joueurs minimum).
- Ensuite vous devez créer un tournoi, choisir le nombre de tours, puis attribuer 8 joueurs à celui-ci.
- Une fois le tournoi créé et sélectionné, vous aller pouvoir démarrer le tournoi ce qui exécutera un nombre de tours préalablement défini.
- À chaque tours, le programme générera des paires de joueurs suivant leur classement. Ensuite, à la fin de chaque tour, vous pourrez entrer les résultats de chaque match.

Une fois le tournoi terminé, vous aurez la possibilité d'afficher les différents rapports du tournoi, de le rejouer, d'en créer un nouveau ou d'en sélectionner un autre.

Pour plus de précisions, veuillez vous référer à la notice d'utilisation qui suit.



# Notice d'utilisation :
Pour démarrer le programme, suivez les [étapes suivantes](https://github.com/A-Nourry/P4_Developpez-un-programme-logiciel-en-Python/wiki#comment-d%C3%A9marrer-lapplication-de-tournoi-d%C3%A9checs) afin de pouvoir exécuter correctement le fichier ***main.py*** du code d'application.

Une fois le programme lancé, vous aurez accès à différents menus.

Pour naviguer dans les différents menus saisissez simplement le chiffre qui correspond à votre choix et préssez la touche ENTRER.


# Description des différents menus:

## Menu principal
```
--------------
MENU PRINCIPAL
--------------
[1] Tournois
[2] Joueurs
[3] Quitter
```
- 1 -- Permet de voir la liste des tournois, d'en ajouter, et de les jouer.
- 2 -- Permet de voir la liste des joueurs et d'en ajouter.
- 3 -- Sélectionnez ce choix si vous souhaitez quitter l'application
  
## 1. Menu Tournoi
```
------------
MENU TOURNOI
------------
[1] Liste des tournois
[2] Nouveau tournoi
[3] Rapport des tournois
[4] Retour
```
- 1 -- Permet de voir la liste des tournois et d'en sélectionner un.
- 2 -- Permet de créer un nouveau tournoi
- 3 -- Permet d'afficher un rapport des tournois créé
- 4 -- Permet de retourner au menu principal

### 1.1 Liste des tournois
```
---------------------------------------------------------------------
LISTE DES TOURNOIS : veuillez sélectionner un tournoi pour commencer.
---------------------------------------------------------------------
[1] -- Tournoi 1
[2] -- Tournoi 2
[3] -- Tournoi 3
...
[n] -- Retour
```
Pour sélectionner un tournoi créé, il suffit d'entrer le choix qui correspond pour accéder au tournoi voulu.

Pour revenir au menu des tournois choisissez **Retour**.

#### 1.1.1 Menu du tournoi selectionné
```
---------------------------------------
MENU DU TOURNOI : *Tournoi sélectionné*
---------------------------------------
[1] Démarrer le tournoi
[2] Joueurs
[3] Tours
[4] Matchs
[5] Description
[6] Retour
```
- 1 -- Permet de démarrer le tournoi :
  - Les tours vont être joués un à un et l'utilisateur pourra entrer les résultats des matchs à la fin de chaque tour.
- 2 -- Permet de voir les joueurs attribués au tournoi.
- 3 -- Permet de voir le rapport des tours joué du tournoi sélectionné.
- 4 -- Permet de voir le rapport des matchs joué du tournoi sélectionné.
- 5 -- Permet de voir ou de modifier la description du tournoi sélectionné.
- 6 -- Permet de revenir à la liste des tournois.
  
##### Joueurs
```
------------------
JOUEURS DU TOURNOI
------------------
[1] Liste des joueurs
[2] Inscription des joueurs
[3] Mise à jour du classement
[4] Retour
```
- 1 -- Permet de voir la liste des joueurs du tournoi.
- 2 -- Permet d'inscrire les joueurs du tournoi
- 3 -- Permet de mettre à jour les classements de chaque joueur
- 4 -- Permet de retourner au menu du tournoi

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
Description:
```
- Nom du tournoi : entrez le nom du tournoi
- Lieu du tournoi : entrez le lieu du tournoi
- Date du tournoi : saisissez la date du tournoi au format xx/xx/xx
- Règle du tournoi ? (bullet, blitz ou speed): saisissez la règle du tournoi.
- Nombre de tours : entrez le nombre de tours pour ce tournoi. Vous devez au minimum mettre 1.
- Description: entrez la description du tournoi.

## 2. Menu Joueurs
```
------------
MENU JOUEURS
------------
[1] Liste des joueurs
[2] Ajouter un joueur
[3] Retour
```
- 1 - Permet d'afficher la liste des joueurs
- 2 - Permet d'ajouter un joueur
- 3 - Permet de retourner au menu principal

# Générer un nouveau fichier flake8-html

Pour générer un fichier flake8-html, il faut commencer par installer le paquet avec la commande:
```
pip install flake8-html
```
Si vous utilisez l'environnement virtuel du code d'application comme expliqué [ici](https://github.com/A-Nourry/P4_Developpez-un-programme-logiciel-en-Python/wiki#comment-d%C3%A9marrer-lapplication-de-tournoi-d%C3%A9checs), le paquet sera déjà présent !

ensuite il suffit de taper la commande suivante pour générer le fichier .html qui contiendra le rapport:
```
flake8 --format=html --htmldir=flake8_rapport --max-line-length 119 --exclude env
```
