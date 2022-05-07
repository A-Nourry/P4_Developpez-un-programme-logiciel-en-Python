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
        self.current_tournament = None

    # Player functions
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

    def update_player_rank(self, player: Player):
        new_player_rank = self.view.prompt_player_rank()
        player.rank == new_player_rank

    def add_players_to_tournament(
        self, player_number, player: Player, tournament: Tournament
    ):
        """add selected Player instance to a selected Tournament instance"""
        tournament.add_player_to_dict(player_number, player)

    def select_tournament_players(self):
        if len(self.players_dict) < self.current_tournament.MAX_NUMBER_PLAYER:
            print("Attention : ")
            print(
                f"Vous devez avoir créé ou chargé au moins {self.current_tournament.MAX_NUMBER_PLAYER} "
                f"joueurs dans le menu principal avant de continuer ! "
                f"({len(self.players_dict)}/{self.current_tournament.MAX_NUMBER_PLAYER})"
            )
            print("")
            input("Appuyer sur ENTRER pour retourner au menu")
        else:
            print(
                f"INSCRIPTION DES {self.current_tournament.MAX_NUMBER_PLAYER} JOUEURS"
            )
            sleep(0.5)
            player_selection = self.menu_view(
                "", *self.players_dict.values(), "Retour"
            )

            player_selection_loop = True

            while player_selection_loop:
                sleep(0.5)
                print(
                    "VEUILLEZ SELECTIONNER LE JOUEUR ",
                    len(self.current_tournament.players) + 1,
                )

                player_choice = player_selection.start_menu()

                if player_choice <= len(self.players_dict):
                    player_index = player_choice
                    selected_player = self.players_dict[player_index]
                    player_number = f"Joueur {player_index}"

                    selection_loop = True
                    while selection_loop:

                        if player_number not in self.current_tournament.players.keys():
                            self.add_players_to_tournament(
                                player_number,
                                selected_player,
                                self.current_tournament,
                            )
                            selection_loop = False

                        else:
                            print(
                                "Ce joueur a déjà été selectionné. Veuillez en choisir un autre"
                            )
                            break

                    if (
                        len(self.current_tournament.players)
                        == self.current_tournament.MAX_NUMBER_PLAYER
                    ):
                        player_selection_loop = False

    def generate_pairs(self, player_dict):
        """generate pairs of players from a dict"""

        first_pair = (player_dict["Joueur 1"], player_dict["Joueur 2"])
        second_pair = (player_dict["Joueur 3"], player_dict["Joueur 4"])
        third_pair = (player_dict["Joueur 5"], player_dict["Joueur 6"])
        fourth_pair = (player_dict["Joueur 7"], player_dict["Joueur 8"])

        return first_pair, second_pair, third_pair, fourth_pair

    # Tournament functions
    def new_tournament(self):
        """instantiate a Tournament object and add it to the controller's tournament dictionnary"""
        new_tournament = self.view.prompt_for_tournament()

        tournament = Tournament(
            name=new_tournament["name"],
            location=new_tournament["location"],
            date=new_tournament["date"],
            time_rule=new_tournament["rule"],
            round_number=new_tournament["round"],
        )

        self.tournament_dict[len(self.tournament_dict)] = tournament

        return tournament

    def start_tournament(self):
        for rounds in range(int(self.current_tournament.round_number)):
            new_round = self.new_round(
                f"Round {rounds + 1}",
                self.current_tournament,
            )
            pairs = self.generate_pairs(self.current_tournament.players)

            print(f"TOUR {rounds + 1}")
            new_round.start_timestamp()
            input(f"Appuyer sur ENTRER pour commencer le tour {rounds + 1}")
            print("Les joueurs suivant doivent s'affrontrer: ")
            sleep(0.5)

            # new match instantiation
            for pair in pairs:
                self.new_match(pair, new_round)
                print(f"{str(pair[0])} contre {str(pair[1])}")

            #  Match start and score
            for matches in new_round.list_of_matches:
                print(matches)
                match = matches
                self.play_match(match)

            sleep(0.5)
            print("--------------")
            print(f"Fin du tour {rounds + 1}")
            print("--------------")
            sleep(0.5)
            new_round.end_timestamp()
            print(
                "début du tour: ",
                new_round.start_time,
            )
            print("Fin du tour: ", new_round.end_time)

        input("Fin du tournoi. Appuyez sur ENTRER pour revenir au menu")

    def add_tournament_description(self):
        self.current_tournament.description = self.view.prompt_description(self.current_tournament)

    # Matches functions
    def new_match(self, pair_of_players, match_round: Round):
        """instantiate Match object and add it to the list of matches from Round object"""

        if match_round is not None:
            match = Match(pair_of_players[0], pair_of_players[1])
            match_round.add_match_to_list(match)

            return True

    def play_match(self, match):
        repr(match)
        match.player_one_result = self.view.prompt_player_score(match.player_one)
        match.player_two_result = self.view.prompt_player_score(match.player_two)

    # Round functions
    def new_round(self, round_number, tournament: Tournament):
        """instantiate Round object add it to the round list from tournament object and return it"""
        if Tournament is not None:
            new_round = Round(f"Round + {round_number}")
            tournament.add_round(new_round)

            return new_round

    #  Menu functions
    def main_menu(self):
        """Start and display the main menu : MENU PRINCIPAL"""

        MAIN_MENU = {
            1: self.menu_tournament,
            2: self.menu_players,
            3: self.menu_save,
            4: self.menu_load,
        }

        loop = True

        while loop:
            menu = self.menu_view(
                "MENU PRINCIPAL",
                "Tournois",
                "Joueurs",
                "Sauvegarder",
                "Charger",
                "Quitter",
            )
            user_input = menu.start_menu()

            if user_input <= len(MAIN_MENU):
                MAIN_MENU[user_input]()
                continue

            else:
                loop = False

    def menu_tournament(self):
        """Starts and displays the sub menu : MENU TOURNOI"""
        MENU_TOURNAMENT = {
            1: self.menu_tournament_list,
            2: self.new_tournament,
            3: self.main_menu,
        }
        loop = True

        while loop:
            menu = self.menu_view(
                "MENU TOURNOI",
                "Liste des tournois",
                "Nouveau tournoi",
                "Retour",
            )
            user_input = menu.start_menu()

            if user_input <= len(MENU_TOURNAMENT):
                MENU_TOURNAMENT[user_input]()
                continue

            elif user_input > len(MENU_TOURNAMENT):
                loop = False

    def menu_players(self):
        menu_player = self.menu_view(
            "MENU JOUEURS", "Liste des joueurs", "Ajouter un joueur", "Retour"
        )

        loop = True

        while loop:
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
                    user_input = input("Voulez vous ajouter un autre joueur ? (y/n)")

                    if user_input == "y":
                        continue
                    else:
                        break

            elif menu_choice == 3:
                loop = False

    def menu_save(self):
        pass

    def menu_load(self):
        pass

    def menu_tournament_list(self):
        print(self.tournament_dict)

        self.current_tournament = None

        loop = True

        if not self.tournament_dict:
            print("il n'y a pas encore de tournois de créé")
            loop = False

        else:
            while loop:
                menu = self.menu_view(
                    "LISTE DES TOURNOIS: Veuillez selectionner un tournoi pour commencer",
                    *self.tournament_dict.values(),
                    "Retour",
                )

                user_input = menu.start_menu()

                if user_input <= len(self.tournament_dict):
                    tournament_index = user_input - 1
                    self.current_tournament = self.tournament_dict[tournament_index]
                    display_current_tournament = repr(self.current_tournament)
                    print(display_current_tournament)

                    if self.current_tournament is not None:
                        self.menu_current_tournament()

                elif user_input >= len(self.tournament_dict):
                    self.menu_tournament()

    def menu_current_tournament(self):
        MENU_CHOICES = {
            1: self.start_tournament,
            2: self.menu_current_tournament_players,
            3: self.menu_current_tournament_rounds,
            4: self.menu_current_tournament_matches,
            5: self.add_tournament_description,
            6: self.menu_tournament_list,
        }

        loop = True

        while loop:
            menu = self.menu_view(
                f"MENU DU TOURNOI: {self.current_tournament}",
                "Démarrer le tournoi",
                "Joueurs",
                "Tours",
                "Matchs",
                "Description",
                "Retour",
            )
            user_input = menu.start_menu()

            if user_input <= len(MENU_CHOICES):
                MENU_CHOICES[user_input]()
                continue

    def menu_current_tournament_players(self):
        menu = self.menu_view(
            "JOUEURS DU TOURNOI",
            "Liste des joueurs",
            "Inscription des joueurs",
            "Retour",
        )

        loop = True
        while loop:

            user_input = menu.start_menu()

            if user_input == 1:
                if not self.current_tournament.players:
                    print("Il n'y a pas encore de joueurs d'inscrit !")
                    continue
                else:
                    current_players = self.current_tournament.players.values()
                    info_players = defaultdict(list)

                    for player in current_players:
                        player_dict = player.display_player()
                        for key, value in player_dict.items():
                            info_players[key].append(value)

                    print(tabulate(info_players, headers="keys"))
                    input("Appuyer sur ENTRER pour revenir au menu")

            elif user_input == 2:
                self.select_tournament_players()

            elif user_input == 3:
                loop = False

    def menu_current_tournament_rounds(self):
        pass

    def menu_current_tournament_matches(self):
        pass

    def current_tournament_description(self):
        pass

    def run(self):
        loop = True

        while loop:
            self.main_menu()
