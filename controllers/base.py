from tabulate import tabulate
from collections import defaultdict
from time import sleep

from models.player import Player, load_players
from models.tournament import Tournament, load_tournaments
from models.match import Match, load_matches
from models.round import Round, load_rounds


class Controller:
    def __init__(self, view, menu_view):
        """Main controller

        Args:
            view (object): main view instance
            menu_view (object): menu instance from view
        """

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
            3: self.tournaments_report,
        }

        self.MENU_CURRENT_TOURNAMENT = {
            1: self.start_tournament,
            2: self.menu_current_tournament_players,
            3: self.current_tournament_rounds_report,
            4: self.current_tournament_matches_report,
            5: self.add_tournament_description,
        }

        # Views
        self.view = view

        # Data
        self.tournament_dict = {}
        self.players_dict = {}
        self.rounds_dict = {}
        self.matches_dict = {}

        self.current_tournament = None

    # Player functions
    def add_player(self):
        """add a new player to the controller players_dict"""
        new_player = self.view.prompt_new_player()
        new_player_id = len(self.players_dict) + 1

        player = Player(
            first_name=new_player["first_name"],
            last_name=new_player["last_name"],
            birth_date=new_player["birth_date"],
            gender=new_player["gender"],
            rank=new_player["rank"],
            p_id=new_player_id,
        )

        self.players_dict[player.p_id] = player
        player.save()

        return True

    def get_players(self):
        """get players arguments from a dict, instantiate them and add them to the controller player dict as objects"""
        players = load_players()

        for player in players:
            new_player = Player(
                first_name=player["first_name"],
                last_name=player["last_name"],
                birth_date=player["birth_date"],
                gender=player["gender"],
                rank=player["rank"],
                p_id=player["p_id"],
            )

            self.players_dict[new_player.p_id] = new_player

    def update_player_rank(self):
        """update player's rank of the current tournament"""
        self.view.display_message("Mise à jour du classement")
        sleep(0.4)

        input_history = []

        for players in self.current_tournament.players.values():
            while True:
                try:
                    new_player_rank = self.view.prompt_player_rank(players)

                    if new_player_rank not in input_history:
                        input_history.append(new_player_rank)
                        players.rank = new_player_rank
                        break

                    elif new_player_rank in input_history:
                        raise ValueError()

                except ValueError:
                    self.view.display_message(
                        "Attention ! Vous avez déjà saisi ce classement pour un autre joueur !"
                    )

    def check_number_of_global_players(self):
        """check if there's an enough amount of global players to begin a tournament's player selection"""
        if len(self.players_dict) < self.current_tournament.MAX_NUMBER_PLAYER:
            self.view.prompt_warning_number_players(
                self.current_tournament.MAX_NUMBER_PLAYER, self.players_dict
            )
            return False
        else:
            return True

    def check_number_of_tournament_players(self):
        """check if there's an enough amount of players in a tournament to start it"""
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
        """Display the global list of players in a menu"""
        if (
            self.check_number_of_global_players()
            and len(self.current_tournament.players)
            < self.current_tournament.MAX_NUMBER_PLAYER
        ):
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

                user_input = player_selection.start_menu()

                if user_input <= len(self.players_dict):
                    selected_player = self.players_dict[user_input]

                    self.add_player_to_tournament(user_input, selected_player.p_id)

                    if (
                        len(self.current_tournament.players)
                        == self.current_tournament.MAX_NUMBER_PLAYER
                    ):
                        player_selection_loop = False

    def add_player_to_tournament(self, user_input, player_id):
        """add a selected player to the current tournament player dict

        Args:
            user_input (int): user input from tournament player selection menu
            player_id (int): player's id (Player.p_id)

        Raises:
            ValueError: if the player is already in the tournament's player dict
        """

        player_number = len(self.current_tournament.players) + 1

        while True:
            try:
                if user_input in self.current_tournament.players.keys():
                    raise ValueError()

                elif user_input not in self.current_tournament.players.keys():
                    self.current_tournament.add_player_id_to_dict(
                        player_number, player_id, self.current_tournament.t_id
                    )
                    break

            except ValueError:
                self.view.display_message(
                    "Ce joueur a déjà été selectionné. Veuillez en choisir un autre"
                )
                break

    def first_round_pairs(self, player_dict):
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
    def check_number_of_tournaments(self):
        """check the number of tournaments in the controller tournament dict"""
        if len(self.tournament_dict) < 1:
            return False
        else:
            return True

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
            description=new_tournament["description"],
            number_of_rounds=new_tournament["round"],
            t_id=len(self.tournament_dict) + 1,
        )

        self.tournament_dict[tournament.t_id] = tournament
        tournament.save()

        return tournament

    def get_tournament(self):
        """instantiate Tournament object from a dict"""

        tournaments = load_tournaments()

        for tournament in tournaments:
            new_tournament = Tournament(
                name=tournament["name"],
                location=tournament["location"],
                date=tournament["date"],
                time_rule=tournament["time_rule"],
                description=tournament["description"],
                max_number_player=tournament["max_number_player"],
                number_of_rounds=tournament["number_of_rounds"],
                t_id=tournament["t_id"],
            )

            new_tournament.players = tournament["players"]
            new_tournament.rounds = tournament["rounds"]

            self.tournament_dict[new_tournament.t_id] = new_tournament

    def instantiate_tournament_players(self, tournament: Tournament):

        for players, player_id in zip(tournament.players, tournament.players.values()):
            tournament.players[players] = self.players_dict[player_id]

    def instantiate_tournament_rounds(self, tournament: Tournament):
        tournament.rounds = [self.rounds_dict[rounds] for rounds in tournament.rounds]

    def start_tournament(self):
        if self.check_number_of_tournament_players():

            if len(self.current_tournament.rounds) > 0:
                self.view.input_message(
                    "Ce tournoi est terminé. Créez en un nouveau dans le menu tournois si vous voulez rejouer !"
                )

            else:
                self.update_player_rank()

                self.generate_tournament_rounds()

                self.instantiate_tournament_rounds(self.current_tournament)
                print(self.rounds_dict)

                print(self.current_tournament.rounds)

                for rounds in self.current_tournament.rounds:
                    print(rounds)

                    self.start_rounds(rounds, rounds)
                    self.first_round(rounds)
                    self.end_rounds(rounds, rounds)

                    self.update_player_rank()

                self.view.input_message(
                    "Fin du tournoi. Appuyez sur ENTRER pour revenir au menu"
                )

    def add_tournament_description(self):
        self.current_tournament.description = self.view.prompt_description(
            self.current_tournament
        )

    # Matches functions
    def new_match(self, player_one, player_two, match_round: Round):
        """instantiates Match object and add it to the controller matches dict
         and adds the match id to the list of matches of a Round object.

        Args:
            pair_of_players (list): list of two players
            match_id (Match.m_id): id of the match
            match_round (Round): Round instance
        """
        new_match_id = len(self.matches_dict) + 1

        if match_round is not None:
            match = Match(player_one.p_id, player_two.p_id, new_match_id)

            match_round.add_match_to_list(match.m_id, match_round.r_id)
            self.matches_dict[match.m_id] = match

            match.save()

            return True

    def get_matches(self):
        matches = load_matches()

        for match in matches:
            new_match = Match(
                player_one=match["player_one"],
                player_two=match["player_two"],
                m_id=match["m_id"],
            )
            new_match.player_one_score = match["player_one_score"]
            new_match.player_two_score = match["player_two_score"]

            self.matches_dict[new_match.m_id] = new_match

    def play_match(self, match):

        # instantiate matches from match id
        match = self.matches_dict[match]

        #  instantiate match's players from player id
        match.player_one = self.current_tournament.players[str(match.player_one)]
        match.player_two = self.current_tournament.players[str(match.player_two)]

        repr(match)

        #  Update players score in match instance
        match.player_one_score += self.view.prompt_player_score(match.player_one)
        match.player_two_score += self.view.prompt_player_score(match.player_two)

        #  Update players instances scores
        match.player_one.score += match.player_one_score
        match.player_two.score += match.player_two_score

        match.update("player_one_score", match.player_one.score)
        match.update("player_two_score", match.player_two.score)

    # Round functions
    def generate_tournament_rounds(self):
        tournament = self.current_tournament

        if tournament is not None:
            for rounds in range(int(tournament.number_of_rounds)):
                new_round_id = len(self.rounds_dict) + 1
                print(rounds)
                new_round = Round(f"Round {rounds + 1}", new_round_id)
                tournament.add_round(new_round.r_id, tournament.t_id)
                print(tournament.rounds)
                self.rounds_dict[new_round.r_id] = new_round

    def get_rounds(self):
        rounds = load_rounds()

        for new_rounds in rounds:
            new_round = Round(
                name=new_rounds["name"],
                r_id=new_rounds["r_id"],
            )
            new_round.list_of_matches = new_rounds["list_of_matches"]
            new_round.start_time = new_rounds["start_time"]
            new_round.end_time = new_rounds["end_time"]

            self.rounds_dict[new_round.r_id] = new_round

    def start_rounds(self, tournament_round, round_number):
        self.view.display_message(f"TOUR {round_number}")

        self.view.input_message(
            f"Appuyer sur ENTRER pour commencer le tour {round_number}"
        )
        tournament_round.start_timestamp()

        self.view.display_message("Les joueurs suivant doivent s'affrontrer: ")
        sleep(0.5)

    def end_rounds(self, tournament_round, round_number):
        sleep(0.5)
        self.view.display_message("--------------")
        self.view.display_message(f"Fin du tour {round_number}")
        self.view.display_message("--------------")
        sleep(0.5)

        tournament_round.end_timestamp()
        tournament_round.save()

        self.view.display_message(f"début du tour: {tournament_round.start_time}")
        self.view.display_message(f"Fin du tour: {tournament_round.end_time}")
        sleep(0.4)

    def first_round(self, new_round):
        pairs = self.first_round_pairs(self.current_tournament.players)

        for pair in pairs:
            self.new_match(pair[0], pair[1], new_round)
            self.view.display_message(f"{str(pair[0])} contre {str(pair[1])}")

        #  Start match and input players scores
        for matches in new_round.list_of_matches:
            self.view.display_message(matches)

            match = matches

            self.view.display_message("------------------")
            self.view.display_message("Saisi des scores :")

            self.play_match(match)

    def instantiate_round_matches(self, current_round: Round):
        current_round.list_of_matches = [
            self.matches_dict[matches] for matches in current_round.list_of_matches
        ]

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

            if user_input in self.MENU_TOURNAMENT.keys():
                self.MENU_TOURNAMENT[user_input]()

            elif user_input == 4:
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
                self.global_players_report()

            elif menu_choice == 2:  # Add a player
                while True:
                    self.add_player()
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

                    self.instantiate_tournament_players(self.current_tournament)
                    self.instantiate_tournament_rounds(self.current_tournament)

                    for rounds in self.current_tournament.rounds:
                        self.instantiate_round_matches(rounds)

                    if self.current_tournament is not None:
                        self.menu_current_tournament()

                elif user_input >= len(self.tournament_dict):
                    loop = False

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

            elif user_input > len(self.MENU_CURRENT_TOURNAMENT):
                loop = False

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
                self.current_tournament_players_report()

            elif user_input == 2:
                self.select_tournament_players()

            elif user_input == 3:
                self.update_player_rank()

            elif user_input == 4:
                loop = False

    def global_players_report(self):
        if not self.players_dict:
            self.view.display_message("Il n'y a pas encore de joueurs de créé !")
        else:
            current_players = self.players_dict.values()
            info_players = defaultdict(list)

            for player in current_players:
                player_dict = player.display_player()
                for key, value in player_dict.items():
                    info_players[key].append(value)

            self.view.display_message(tabulate(info_players, headers="keys", tablefmt="grid"))
            self.view.input_message("Appuyer sur ENTRER pour revenir au menu")

    def tournaments_report(self):
        if not self.tournament_dict:
            self.view.display_message("Il n'y a pas encore de tournoi de créé !")
        else:
            tournaments = self.tournament_dict.values()
            info_tournaments = defaultdict(list)

            for tournament in tournaments:
                tournament_dict = tournament.display_tournament()
                for key, value in tournament_dict.items():
                    info_tournaments[key].append(value)

            self.view.display_message(tabulate(info_tournaments, headers="keys", tablefmt="grid"))
            self.view.input_message("Appuyer sur ENTRER pour revenir au menu")

    def current_tournament_rounds_report(self):
        if not self.current_tournament.rounds:
            self.view.display_message("Le tournoi n'a pas encore été joué !")
        else:
            tournament_rounds = self.current_tournament.rounds
            info_rounds = defaultdict(list)

            for tournament_round in tournament_rounds:
                round_dict = tournament_round.display_round()
                for key, value in round_dict.items():
                    info_rounds[key].append(value)

            self.view.display_message(tabulate(info_rounds, headers="keys", tablefmt="grid"))
            self.view.input_message("Appuyer sur ENTRER pour revenir au menu")

    def current_tournament_matches_report(self):
        if not self.current_tournament.rounds:
            self.view.display_message("Le tournoi n'a pas encore été joué !")
        else:
            info_matches = defaultdict(list)
            for rounds in self.current_tournament.rounds:

                for matches in rounds.list_of_matches:
                    match_dict = matches.display_match_result()
                    for key, value in match_dict.items():
                        info_matches[key].append(value)

                self.view.display_message(tabulate(info_matches, headers="keys", tablefmt="grid"))
            self.view.input_message("Appuyer sur ENTRER pour revenir au menu")

    def current_tournament_players_report(self):
        if not self.current_tournament.players:
            self.view.display_message("Il n'y a pas encore de joueurs d'inscrit !")
        else:
            current_players = self.current_tournament.players.values()
            info_players = defaultdict(list)

            for player in current_players:
                player_dict = player.display_player()
                for key, value in player_dict.items():
                    info_players[key].append(value)

            self.view.display_message(tabulate(info_players, headers="keys", tablefmt="grid"))
            self.view.input_message("Appuyer sur ENTRER pour revenir au menu")

    def run(self):
        self.get_players()
        self.get_tournament()
        self.get_rounds()
        self.get_matches()

        self.main_menu()
