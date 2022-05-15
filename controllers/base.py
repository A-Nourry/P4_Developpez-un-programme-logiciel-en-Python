from tabulate import tabulate
from collections import defaultdict
from time import sleep

from models.player import Player, load_players
from models.tournament import Tournament, load_tournaments
from models.match import Match
from models.round import Round


class Controller:
    def __init__(self, view, menu_view):

        # Menus
        self.menu_view = menu_view

        self.MAIN_MENU = {
            1: self.menu_tournament,
            2: self.menu_players,
            3: self.menu_options,
        }

        self.MENU_TOURNAMENT = {
            1: self.menu_tournament_list,
            2: self.new_tournament,
            3: self.report_tournaments,
            4: self.main_menu,
        }

        self.MENU_CURRENT_TOURNAMENT = {
            1: self.start_tournament,
            2: self.menu_current_tournament_players,
            3: self.report_current_tournament_rounds,
            4: self.report_current_tournament_matches,
            5: self.add_tournament_description,
            6: self.menu_tournament_list,
        }

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
        player.save()

        return True

    def get_players(self):
        players = load_players()

        for player in players:
            player = Player(
                first_name=player["Prénom"],
                last_name=player["Nom"],
                birth_date=player["Date de naissance"],
                gender=player["Sexe"],
                rank=player["Classement"],
            )

            self.players_dict[len(self.players_dict) + 1] = player

    def update_player_rank(self):
        for players in self.current_tournament.players.values():
            new_player_rank = self.view.prompt_player_rank(players)
            players.rank = new_player_rank

    def add_players_to_tournament(
        self, player_number, player: Player, tournament: Tournament
    ):
        """add selected Player instance to a selected Tournament instance"""
        tournament.add_player_to_dict(player_number, player)
        player.score = 0.0

    def check_number_of_global_players(self):
        if len(self.players_dict) < self.current_tournament.MAX_NUMBER_PLAYER:
            self.view.prompt_warning_number_players(
                self.current_tournament.MAX_NUMBER_PLAYER, self.players_dict
            )
            return False
        else:
            return True

    def check_number_of_tournament_players(self):
        if (
            len(self.current_tournament.players)
            < self.current_tournament.MAX_NUMBER_PLAYER
        ):
            self.view.display_message(
                f"Vous devez avoir inscrit {self.current_tournament.MAX_NUMBER_PLAYER} "
                f"joueurs avant de commencer le tournoi !"
            )
            self.view.input_message("Appuyer sur ENTRER pour continuer")
            return False
        else:
            return True

    def select_tournament_players(self):
        if self.check_number_of_global_players():
            self.view.display_message(
                "Attention les scores des joueurs seront remis à 0 !"
            )
            self.view.input_message("Appuyer sur ENTRER pour continuer")

            player_selection = self.menu_view("", *self.players_dict.values(), "Retour")

            self.view.display_message(
                f"INSCRIPTION DES {self.current_tournament.MAX_NUMBER_PLAYER} JOUEURS"
            )

            player_selection_loop = True

            while player_selection_loop:
                sleep(0.5)
                self.view.display_message(
                    f"VEUILLEZ SELECTIONNER LE JOUEUR {len(self.current_tournament.players) + 1}"
                )

                player_choice = player_selection.start_menu()

                if player_choice <= len(self.players_dict):
                    selected_player = self.players_dict[player_choice]
                    player_number = f"Joueur {player_choice}"

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
                            self.view.display_message(
                                "Ce joueur a déjà été selectionné. Veuillez en choisir un autre"
                            )
                            break

                    if (
                        len(self.current_tournament.players)
                        == self.current_tournament.MAX_NUMBER_PLAYER
                    ):
                        player_selection_loop = False

    def generate_pairs(self, player_dict):
        """generate pairs of players by ranks, from a dict"""
        upper_list = []
        lower_list = []

        for player in player_dict.values():
            if player.rank < 5:
                upper_list.append(player)
            else:
                lower_list.append(player)

        list_of_pairs = []

        for players in zip(upper_list, lower_list):
            list_of_pairs.append(players)

        first_pair = list_of_pairs[0]
        second_pair = list_of_pairs[1]
        third_pair = list_of_pairs[2]
        fourth_pair = list_of_pairs[3]

        return first_pair, second_pair, third_pair, fourth_pair

    # Tournament functions
    def new_tournament(self):
        """instantiate a Tournament object and add it to the controller's tournament dictionnary"""
        sleep(0.3)
        self.view.display_message("Création d'un nouveau tournoi : ")
        new_tournament = self.view.prompt_for_tournament()

        tournament = Tournament(
            name=new_tournament["name"],
            location=new_tournament["location"],
            date=new_tournament["date"],
            time_rule=new_tournament["rule"],
            round_number=new_tournament["round"],
        )

        self.tournament_dict[len(self.tournament_dict) + 1] = tournament
        tournament.save()

        return tournament

    def get_tournament(self):
        tournaments = load_tournaments()

        for tournament in tournaments:
            tournament = Tournament(
                name=tournament["Nom"],
                location=tournament["Lieu"],
                date=tournament["Date"],
                time_rule=tournament["Règle du temps"],
                max_number_player=tournament["Nombre de joueurs"],
                round_number=tournament["Nombre de tours"],
            )

        self.tournament_dict[len(self.tournament_dict) + 1] = tournament

    def start_tournament(self):
        if self.check_number_of_tournament_players():
            for rounds in range(int(self.current_tournament.round_number)):
                new_round = self.new_round(
                    f"Round {rounds + 1}",
                    self.current_tournament,
                )
                pairs = self.generate_pairs(self.current_tournament.players)

                self.view.display_message(f"TOUR {rounds + 1}")
                new_round.start_timestamp()
                self.view.input_message(
                    f"Appuyer sur ENTRER pour commencer le tour {rounds + 1}"
                )
                self.view.display_message("Les joueurs suivant doivent s'affrontrer: ")
                sleep(0.5)

                # new match instantiation
                for pair in pairs:
                    self.new_match(pair, new_round)
                    self.view.display_message(f"{str(pair[0])} contre {str(pair[1])}")

                #  Match start and score
                for matches in new_round.list_of_matches:
                    self.view.display_message(matches)
                    match = matches
                    self.view.display_message("------------------")
                    self.view.display_message("Saisi des scores :")
                    self.play_match(match)

                sleep(0.5)
                self.view.display_message("--------------")
                self.view.display_message(f"Fin du tour {rounds + 1}")
                self.view.display_message("--------------")
                sleep(0.5)
                new_round.end_timestamp()
                self.view.display_message(f"début du tour: {new_round.start_time}")
                self.view.display_message(f"Fin du tour: {new_round.end_time}")
                sleep(0.4)
                self.view.display_message("Mise à jour du classement")
                sleep(0.4)
                self.update_player_rank()

            self.view.input_message(
                "Fin du tournoi. Appuyez sur ENTRER pour revenir au menu"
            )

    def add_tournament_description(self):
        self.current_tournament.description = self.view.prompt_description(
            self.current_tournament
        )

    # Matches functions
    def new_match(self, pair_of_players, match_round: Round):
        """instantiate Match object and add it to the list of matches from Round object"""

        if match_round is not None:
            match = Match(pair_of_players[0], pair_of_players[1])
            match_round.add_match_to_list(match)
            match.save()

            return True

    def play_match(self, match):
        repr(match)

        #  Update players score in match instance
        match.player_one_score += self.view.prompt_player_score(match.player_one)
        match.player_two_score += self.view.prompt_player_score(match.player_two)

        #  Update players instances scores
        match.player_one.score += match.player_one_score
        match.player_two.score += match.player_two_score

    # Round functions
    def new_round(self, round_number, tournament: Tournament):
        """instantiate Round object add it to the round list from tournament object and return it"""
        if tournament is not None:
            new_round = Round(f"{round_number}")
            tournament.add_round(new_round)
            new_round.save()

            return new_round

    #  Menu functions
    def main_menu(self):
        """Start and display the main menu : MENU PRINCIPAL"""

        loop = True

        while loop:
            menu = self.menu_view(
                "MENU PRINCIPAL",
                "Tournois",
                "Joueurs",
                "Options",
                "Quitter",
            )
            user_input = menu.start_menu()

            if user_input in self.MAIN_MENU.keys():
                self.MAIN_MENU[user_input]()
                continue

            elif user_input == 4:
                loop = False

    def menu_tournament(self):
        """Starts and displays the sub menu : MENU TOURNOI"""

        loop = True

        while loop:
            menu = self.menu_view(
                "MENU TOURNOI",
                "Liste des tournois",
                "Nouveau tournoi",
                "Rapport des tournois",
                "Retour",
            )
            user_input = menu.start_menu()

            if user_input <= len(self.MENU_TOURNAMENT):
                self.MENU_TOURNAMENT[user_input]()
                continue

            elif user_input > len(self.MENU_TOURNAMENT):
                loop = False

    def menu_players(self):
        menu_player = self.menu_view(
            "MENU JOUEURS",
            "Liste des joueurs",
            "Ajouter un joueur",
            "Retour",
        )

        loop = True

        while loop:
            menu_choice = menu_player.start_menu()

            if menu_choice == 1:  # Show global player list
                if not self.players_dict:
                    self.view.display_message(
                        "Il n'y a pas encore de joueurs de créé !"
                    )
                    continue
                else:
                    current_players = self.players_dict.values()
                    info_players = defaultdict(list)

                    for player in current_players:
                        player_dict = player.display_player()
                        for key, value in player_dict.items():
                            info_players[key].append(value)

                    self.view.display_message(tabulate(info_players, headers="keys"))
                    self.view.input_message("Appuyer sur ENTRER pour revenir au menu")

            elif menu_choice == 2:  # Add a player
                while True:
                    self.add_player(len(self.players_dict) + 1)
                    user_input = self.view.input_message(
                        "Voulez vous ajouter un autre joueur ? (y: oui / n: non)"
                    )

                    if user_input == "y":
                        continue
                    else:
                        break

            elif menu_choice == 3:
                loop = False

    def menu_options(self):
        menu_options = self.menu_view(
            "MENU OPTIONS",
            "Supprimer tous les joueurs",
            "Retour",
        )

        loop = True

        while loop:
            menu_choice = menu_options.start_menu()

            if menu_choice == 1:
                choice = self.view.input_message(
                    "Etes vous sur de vouloir supprimer tous les joueurs ? (y: oui / n: non)"
                )
                if choice == "y":
                    sleep(1)
                    self.players_dict = {}
                    self.view.display_message("Les joueurs ont bien été supprimé")
                    sleep(1)

                elif choice == "n":
                    continue
                else:
                    self.view.display_message("Saisissez 'y' ou 'n' pour continuer")

            elif menu_choice == 2:
                loop = False

    def menu_tournament_list(self):

        self.current_tournament = None

        loop = True

        if not self.tournament_dict:
            self.view.display_message("il n'y a pas encore de tournois de créé !")
            self.view.input_message("Appuyer sur ENTRER pour continuer")
            loop = False

        else:
            while loop:
                menu = self.menu_view(
                    "LISTE DES TOURNOIS: Veuillez selectionner un tournoi pour commencer",
                    *self.tournament_dict.values(),
                    "Retour",
                )

                user_input = menu.start_menu()

                if user_input in self.tournament_dict.keys():
                    tournament_index = user_input
                    self.current_tournament = self.tournament_dict[tournament_index]
                    display_current_tournament = repr(self.current_tournament)
                    self.view.display_message(display_current_tournament)

                    if self.current_tournament is not None:
                        self.menu_current_tournament()

                elif user_input >= len(self.tournament_dict):
                    self.menu_tournament()

    def menu_current_tournament(self):

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

            if user_input in self.MENU_CURRENT_TOURNAMENT.keys():
                self.MENU_CURRENT_TOURNAMENT[user_input]()
                continue

    def menu_current_tournament_players(self):
        menu = self.menu_view(
            "JOUEURS DU TOURNOI",
            "Liste des joueurs",
            "Inscription des joueurs",
            "Mise à jour du classement",
            "Retour",
        )

        loop = True
        while loop:

            user_input = menu.start_menu()

            if user_input == 1:
                if not self.current_tournament.players:
                    self.view.display_message(
                        "Il n'y a pas encore de joueurs d'inscrit !"
                    )
                    continue
                else:
                    current_players = self.current_tournament.players.values()
                    info_players = defaultdict(list)

                    for player in current_players:
                        player_dict = player.display_player()
                        for key, value in player_dict.items():
                            info_players[key].append(value)

                    self.view.display_message(tabulate(info_players, headers="keys"))
                    self.view.input_message("Appuyer sur ENTRER pour revenir au menu")

            elif user_input == 2:
                self.select_tournament_players()

            elif user_input == 3:
                self.update_player_rank()

            elif user_input == 4:
                loop = False

    def report_tournaments(self):
        if not self.tournament_dict:
            self.view.display_message("Il n'y a pas encore de tournoi de créé !")
        else:
            tournaments = self.tournament_dict.values()
            info_tournaments = defaultdict(list)

            for tournament in tournaments:
                tournament_dict = tournament.display_tournament()
                for key, value in tournament_dict.items():
                    info_tournaments[key].append(value)

            self.view.display_message(tabulate(info_tournaments, headers="keys"))
            self.view.input_message("Appuyer sur ENTRER pour revenir au menu")

    def report_current_tournament_rounds(self):
        if not self.current_tournament.rounds:
            self.view.display_message("Le tournoi n'a pas encore été joué !")
        else:
            tournament_rounds = self.current_tournament.rounds
            info_rounds = defaultdict(list)

            for tournament_round in tournament_rounds:
                round_dict = tournament_round.display_round()
                for key, value in round_dict.items():
                    info_rounds[key].append(value)

            self.view.display_message(tabulate(info_rounds, headers="keys"))
            self.view.input_message("Appuyer sur ENTRER pour revenir au menu")

    def report_current_tournament_matches(self):
        if not self.current_tournament.rounds:
            self.view.display_message("Le tournoi n'a pas encore été joué !")
        else:
            info_matches = defaultdict(list)
            for rounds in self.current_tournament.rounds:

                for matches in rounds.list_of_matches:
                    match_dict = matches.display_match_result()
                    for key, value in match_dict.items():
                        info_matches[key].append(value)

            self.view.display_message(tabulate(info_matches, headers="keys"))
            self.view.input_message("Appuyer sur ENTRER pour revenir au menu")

    def run(self):
        self.get_players()
        self.get_tournament()

        self.main_menu()
