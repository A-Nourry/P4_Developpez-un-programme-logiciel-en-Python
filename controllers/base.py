from tabulate import tabulate
from collections import defaultdict
from time import sleep

from models.player import Player
from models.tournament import Tournament
from models.match import Match
from models.round import Round


class Controller:
    def __init__(self, view, menu_view):

        # Menus
        self.menu_view = menu_view

        # Views
        self.view = view

        # Data
        self.tournament_dict = {}
        self.players_dict = {}

    def add_player(self, player_number):
        """add a new player to the data base"""
        new_player = self.view.prompt_new_player()

        player = Player(
            first_name=new_player["first_name"],
            last_name=new_player["last_name"],
            birth_date=new_player["birth_date"],
            gender=new_player["gender"],
            rank=new_player["rank"],
        )

        self.players_dict[player_number] = player

        return True

    def add_players_to_tournament(self, player_number, player: Player, tournament: Tournament):
        """add selected Player instance to a selected Tournament instance"""
        tournament.add_player_to_dict(player_number, player)

    def new_tournament(self, tournament_number):
        """instantiate a Tournament object and add it to the controller's tournament dictionnary"""
        new_tournament = self.view.prompt_for_tournament()

        tournament = Tournament(
            name=new_tournament["name"],
            location=new_tournament["location"],
            date=new_tournament["date"],
            time_rule=new_tournament["rule"],
            round_number=new_tournament["round"],
        )

        self.tournament_dict[tournament_number] = tournament

        return tournament

    def add_tournament_description(self, tournament: Tournament):
        tournament.description = self.view.prompt_description()

    def generate_pairs(self, player_dict):
        """generate pairs of players from a dict"""

        first_pair = (player_dict["Joueur 1"], player_dict["Joueur 2"])
        second_pair = (player_dict["Joueur 3"], player_dict["Joueur 4"])
        third_pair = (player_dict["Joueur 5"], player_dict["Joueur 6"])
        fourth_pair = (player_dict["Joueur 7"], player_dict["Joueur 8"])

        return first_pair, second_pair, third_pair, fourth_pair

    def new_match(self, pair_of_players, match_round: Round):
        """instantiate Match object and add it to the list of matches from Round object"""

        if match_round is not None:
            match = Match(pair_of_players[0], pair_of_players[1])
            match_round.add_match_to_list(match)

            return True

    def new_round(self, round_number, tournament: Tournament):
        """instantiate Round object add it to the round list from tournament object and return it"""
        if Tournament is not None:
            new_round = Round(f"Round + {round_number}")
            tournament.add_round(new_round)

            return new_round

    def run(self):
        menu = self.menu_view(
            "MENU PRINCIPAL",
            "Tournois",
            "Joueurs",
            "Sauvegarder",
            "Charger",
            "Quitter",
        )
        menu_tournoi = self.menu_view(
            "MENU TOURNOI",
            "Liste des tournois",
            "Nouveau tournoi",
            "Retour",
        )

        menu_player = self.menu_view(
            "MENU JOUEURS", "Liste des joueurs", "Ajouter un joueur", "Retour"
        )

        # Main menu
        loop = True

        while loop:
            menu_choice = menu.start_menu()

            if menu_choice == 1:

                sub_loop = True

                # Tournament menu
                while sub_loop:
                    menu_choice = menu_tournoi.start_menu()

                    if menu_choice == 1:

                        tournament_loop = True

                        if not self.tournament_dict:
                            print("il n'y a pas encore de tournois de créé")
                            tournament_loop = False

                        else:

                            # List of tournament menu
                            while tournament_loop:
                                menu_list_tournois = self.menu_view(
                                    "LISTE DES TOURNOIS: Veuillez selectionner un tournoi pour commencer",
                                    *self.tournament_dict.values(),
                                    "Retour",
                                )

                                menu_choice = menu_list_tournois.start_menu()

                                if menu_choice <= len(self.tournament_dict):
                                    tournament_index = menu_choice - 1
                                    current_tournament = self.tournament_dict[
                                        tournament_index
                                    ]
                                    display_current_tournament = repr(
                                        current_tournament
                                    )

                                    sub_tournament_loop = True

                                    # current tournament menu
                                    while sub_tournament_loop:
                                        sub_menu_tournament = self.menu_view(
                                            f"MENU DU TOURNOI: {display_current_tournament}",
                                            "Démarrer le tournoi",
                                            "Joueurs",
                                            "Tours",
                                            "Matchs",
                                            "Description",
                                            "Retour",
                                        )

                                        menu_choice = sub_menu_tournament.start_menu()

                                        if menu_choice == 1:  # Start tournament
                                            for rounds in range(
                                                int(current_tournament.round_number)
                                            ):
                                                new_round = self.new_round(
                                                    f"Round {rounds + 1}",
                                                    current_tournament,
                                                )
                                                pairs = self.generate_pairs(
                                                    current_tournament.players
                                                )

                                                print(f"TOUR {rounds + 1}")
                                                new_round.start_timestamp()
                                                input(
                                                    f"Appuyer sur ENTRER pour commencer le tour {rounds + 1}"
                                                )
                                                print(
                                                    "Les joueurs suivant doivent s'affrontrer: "
                                                )
                                                sleep(1)

                                                for pair in pairs:
                                                    self.new_match(pair, new_round)
                                                    print(
                                                        f"{str(pair[0])} contre {str(pair[1])}"
                                                    )

                                                input(
                                                    "Appuyer sur ENTRER pour saisir les résultats"
                                                )

                                                for (
                                                    matches
                                                ) in new_round.list_of_matches:
                                                    print(matches)
                                                    match = matches
                                                    match.play_match()

                                                sleep(1)
                                                print("--------------")
                                                print(f"Fin du tour {rounds + 1}")
                                                print("--------------")
                                                sleep(1)
                                                new_round.end_timestamp()
                                                print(
                                                    "début du tour: ",
                                                    new_round.start_time,
                                                )
                                                print(
                                                    "Fin du tour: ", new_round.end_time
                                                )

                                            input(
                                                "Fin du tournoi. Appuyez sur ENTRER pour revenir au menu"
                                            )

                                        elif menu_choice == 2:  # Show players
                                            tournament_players = (
                                                current_tournament.players.values()
                                            )
                                            info_players = defaultdict(list)

                                            for player in tournament_players:
                                                player_dict = player.display_player()
                                                for key, value in player_dict.items():
                                                    info_players[key].append(value)

                                            print(
                                                tabulate(info_players, headers="keys")
                                            )
                                            input(
                                                "Appuyer sur ENTRER pour revenir au menu"
                                            )

                                        elif menu_choice == 3:  # Show rounds
                                            tournament_rounds = (
                                                current_tournament.rounds
                                            )
                                            if not tournament_rounds:
                                                print(
                                                    "Aucun tours n'ont été joué. Démarrez le tournoi"
                                                )

                                        elif menu_choice == 5:  # Tournament Description
                                            print(current_tournament.description)
                                            self.add_tournament_description(current_tournament)

                                        elif menu_choice == 6:  # Back to parent menu
                                            sub_tournament_loop = False

                                elif menu_choice == len(self.tournament_dict) + 1:
                                    tournament_loop = False

                    elif menu_choice == 2:

                        print("NOUVEAU TOURNOI")
                        tournament = self.new_tournament(len(self.tournament_dict))

                        print(f"ATTRIBUTION DES {tournament.MAX_NUMBER_PLAYER} JOUEURS")
                        player_selection = self.menu_view(
                            "AJOUTER UN JOUEUR:", *self.players_dict.values(), "Retour"
                        )

                        player_selection_loop = True

                        while player_selection_loop:
                            print(
                                    "Veuillez selectionner le joueur",
                                    len(tournament.players) + 1,
                                )

                            player_choice = player_selection.start_menu()

                            if player_choice <= len(self.players_dict):
                                player_index = player_choice
                                selected_player = self.players_dict[player_index]
                                player_number = f"Joueur {player_index}"

                                selection_loop = True
                                while selection_loop:

                                    if player_number not in tournament.players.keys():
                                        self.add_players_to_tournament(
                                            player_number,
                                            selected_player,
                                            tournament,
                                        )
                                        selection_loop = False

                                    else:
                                        print(
                                            "Ce joueur a déjà été selectionné. Veuillez en choisir un autre"
                                        )
                                        break

                                if (
                                    len(tournament.players) == tournament.MAX_NUMBER_PLAYER
                                ):
                                    player_selection_loop = False

                    elif menu_choice == 3:
                        sub_loop = False

            elif menu_choice == 2:  # Menu Player
                sub_loop = True

                while sub_loop:
                    menu_choice = menu_player.start_menu()

                    if menu_choice == 1:  # Show global player list
                        if not self.players_dict:
                            print("Il n'y a pas encore de joueurs de créé !")
                            continue
                        else:
                            current_players = self.players_dict.values()
                            info_players = defaultdict(list)

                            for player in current_players:
                                player_dict = player.display_player()
                                for key, value in player_dict.items():
                                    info_players[key].append(value)

                            print(tabulate(info_players, headers="keys"))
                            input("Appuyer sur ENTRER pour revenir au menu")

                    elif menu_choice == 2:  # Add a player
                        while True:
                            self.add_player(len(self.players_dict) + 1)
                            user_input = input(
                                "Voulez vous ajouter un autre joueur ? (y/n)"
                            )

                            if user_input == "y":
                                continue
                            else:
                                break

                    elif menu_choice == 3:
                        sub_loop = False

            elif menu_choice == 4:
                loop = False
