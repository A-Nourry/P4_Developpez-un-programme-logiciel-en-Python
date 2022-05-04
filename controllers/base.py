from tabulate import tabulate
from collections import defaultdict

from models.player import Player
from models.tournament import Tournament
from models.match import Match
from models.round import Round
from views.menu import Menu


class Controller:
    def __init__(self, view):

        # Menus

        # views
        self.view = view

        self.tournament_dict = {}

    def add_player(self, player_number, tournament: Tournament):
        """add a new player to the player dict from a Tournament object"""
        if tournament is not None:
            new_player = self.view.prompt_new_player()

            player = Player(
                first_name=new_player["first_name"],
                last_name=new_player["last_name"],
                birth_date=new_player["birth_date"],
                gender=new_player["gender"],
                rank=new_player["rank"],
            )

            tournament.add_player_to_dict(player_number, player)

            return True

    def new_tournament(self, tournament_number):
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
        menu = Menu("MENU PRINCIPALE", "Tournois", "Sauvegarder", "Charger", "Quitter")
        menu_tournoi = Menu(
            "MENU TOURNOI",
            "Liste des tournois",
            "Nouveau tournoi",
            "Retour",
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
                                menu_list_tournois = Menu(
                                    "LISTE DES TOURNOIS",
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
                                        sub_menu_tournament = Menu(
                                            f"MENU : {display_current_tournament}",
                                            "Démarrer le tournoi",
                                            "Joueurs",
                                            "Tours",
                                            "Matchs",
                                            "Description",
                                            "Retour",
                                        )

                                        menu_choice = sub_menu_tournament.start_menu()

                                        if menu_choice == 1:  # Start tournament
                                            for rounds in range(int(current_tournament.round_number)):
                                                new_round = self.new_round(f"Round {rounds + 1}", current_tournament)
                                                pairs = self.generate_pairs(current_tournament.players)
                                                print(f"TOUR {rounds + 1}")
                                                print("Les joueurs suivant doivent s'affrontrer: ")

                                                for pair in pairs:
                                                    self.new_match(pair, new_round)
                                                    print(f"{str(pair[0])} contre {str(pair[1])}")

                                                input("Appuyer sur ENTRER pour saisir les résultats")

                                                for matches in new_round.list_of_matches:
                                                    print(matches)
                                                    match = matches
                                                    match.play_match()

                                                print(f"Fin du tour {rounds + 1}")
                                            input("Fin du tournoi. Appuyez sur ENTRER pour revenir au menu")

                                        elif menu_choice == 2:  # Show players
                                            tournament_players = current_tournament.players.values()
                                            info_players = defaultdict(list)

                                            for player in tournament_players:
                                                player_dict = player.display_player()
                                                for key, value in player_dict.items():
                                                    info_players[key].append(value)

                                            print(tabulate(info_players, headers="keys"))
                                            input("Appuyer sur ENTRER pour revenir au menu")

                                        elif menu_choice == 3:
                                            tournament_rounds = current_tournament.rounds
                                            print(tournament_rounds)

                                        elif menu_choice == 6:  # Back to parent menu
                                            sub_tournament_loop = False

                                elif menu_choice == len(self.tournament_dict) + 1:
                                    tournament_loop = False

                    elif menu_choice == 2:

                        print("NOUVEAU TOURNOI")
                        tournament = self.new_tournament(len(self.tournament_dict))

                        print(f"AJOUT DES {tournament.MAX_NUMBER_PLAYER} JOUEURS")
                        for i in range(tournament.MAX_NUMBER_PLAYER):
                            player_number = f"Joueur {i + 1}"
                            print("JOUEUR", i + 1)
                            self.add_player(player_number, tournament)

                        continue

                    elif menu_choice == 3:
                        sub_loop = False

            elif menu_choice == 2:
                sub_loop = True

                while sub_loop:
                    menu_choice = "mettre un menu"

                    if menu_choice == 0:
                        continue

                    if menu_choice == 1:
                        sub_loop = False

            elif menu_choice == 4:
                loop = False
