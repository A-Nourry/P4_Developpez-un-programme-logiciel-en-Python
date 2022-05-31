from tabulate import tabulate
from collections import defaultdict
from time import sleep

from models.player import Player
from models.tournament import Tournament
from models.match import Match
from models.round import Round


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
            5: self.tournament_description,
        }

        # Views
        self.view = view

        # Data
        self.tournament_dict = {}
        self.players_dict = {}
        self.rounds_dict = {}
        self.matches_dict = {}

        self.current_tournament = None

    def erase_all_dict(self):
        """reset all dicts of the controller"""

        self.players_dict = {}
        self.tournament_dict = {}
        self.rounds_dict = {}
        self.matches_dict = {}

    def load_all_data(self):
        """loads all instances from the data base and and them to the controller dicts"""

        self.get_players()
        self.get_tournament()
        self.get_rounds()
        self.get_matches()

        return True

    def save_all_data(self):
        """saves all instances of the controller's dicts"""

        for players in self.players_dict.values():
            players.save()

        for tournaments in self.tournament_dict.values():
            tournaments.save()

        for rounds in self.rounds_dict.values():
            rounds.save()

        for matches in self.matches_dict.values():
            matches.save()

    def erase_all_data(self):
        """erase all the saved data"""

        Player.erase_data()
        Tournament.erase_data()
        Round.erase_data()
        Match.erase_data()

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

        return True

    def get_players(self):
        """get players arguments from a dict, instantiate them and add them to the controller player dict as objects"""
        players = Player.load_players()

        for player in players:
            new_player = Player(
                first_name=player["first_name"],
                last_name=player["last_name"],
                birth_date=player["birth_date"],
                gender=player["gender"],
                rank=player["rank"],
                p_id=player["p_id"],
            )

            new_player.match_score = player["match_score"]

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
                        players.update("rank", players.rank)
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
        """displays players to select them"""
        if (
            self.check_number_of_global_players()
            and len(self.current_tournament.players)
            < self.current_tournament.MAX_NUMBER_PLAYER
        ):
            player_selection = self.menu_view(
                "JOUEURS", *self.players_dict.values(), "Retour"
            )

            self.view.display_message(
                f"INSCRIPTION DES {self.current_tournament.MAX_NUMBER_PLAYER} JOUEURS : "
            )

            player_selection_loop = True

            while player_selection_loop:
                sleep(0.5)
                self.view.display_message(
                    f"Veuillez sélectionner le joueur {len(self.current_tournament.players) + 1}"
                )

                user_input = player_selection.start_menu()

                if user_input in self.current_tournament.players.values():
                    self.view.display_message(
                        "ce joueur a déjà été sélectionné ! Veuillez en choisir un autre"
                    )
                    continue

                elif user_input <= len(self.players_dict):
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

        player_number = f"{len(self.current_tournament.players) + 1}"

        while True:
            try:
                if user_input in self.current_tournament.players.keys():
                    raise ValueError()

                elif user_input not in self.current_tournament.players.keys():
                    self.current_tournament.add_player_id_to_dict(
                        player_number, player_id
                    )
                    break

            except ValueError:
                self.view.display_message(
                    "Ce joueur a déjà été selectionné. Veuillez en choisir un autre"
                )
                break

    def first_round_pairs(self, player_dict):
        """generate pairs of players by ranks

        Args:
            player_dict (dict): dict of players, of a Tournament instance

        Returns:
            tuples: returns four pairs of players
        """
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

    def round_pairs(self, player_dict):
        """generates pairs of players by score and ranks

        Args:
            player_dict (dict): dict of players, of a Tournament instance

        Returns:
            tuples: returns four pairs of players
        """
        list_of_players = []

        for player in player_dict.values():
            list_of_players.append(player)

        list_of_players.sort(key=lambda x: (x.match_score, -x.rank), reverse=True)

        first_pair = (list_of_players[0], list_of_players[1])
        second_pair = (list_of_players[2], list_of_players[3])
        third_pair = (list_of_players[4], list_of_players[5])
        fourth_pair = (list_of_players[6], list_of_players[7])

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

        return tournament

    def get_tournament(self):
        """instantiate Tournament object from a dict"""

        tournaments = Tournament.load_tournaments()

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

    def get_tournament_players_instances(self, tournament: Tournament):
        """converts Tournament Player ids to Player instances from the controller player dict

        Args:
            tournament (Tournament): Tournament instance
        """

        for players, player_id in zip(tournament.players, tournament.players.values()):
            tournament.players[players] = self.players_dict[player_id]

    def get_tournament_players_ids(self, tournament: Tournament):
        """converts Tournament Player instances to Player ids

        Args:
            tournament (Tournament): Tournament instance
        """

        for key, players in zip(tournament.players, tournament.players.values()):
            tournament.players[key] = players.p_id

    def get_tournament_rounds_instances(self, tournament: Tournament):
        """converts Tournament Round ids to Round instances from the controller round dict

        Args:
            tournament (Tournament): Tournament instance
        """
        tournament.rounds = [self.rounds_dict[rounds] for rounds in tournament.rounds]

    def get_tournament_rounds_ids(self, tournament: Tournament):
        """converts Tournament Round instances to Round ids

        Args:
            tournament (Tournament): Tournament instance
        """
        tournament.rounds = [rounds.r_id for rounds in tournament.rounds]

    def start_tournament(self):
        """starts the main tournament"""
        if self.check_number_of_tournament_players():

            if (
                len(self.current_tournament.rounds) > 0
            ):  # check if the tournament already have rounds
                self.view.input_message(
                    "Ce tournoi est terminé. Créez en un nouveau dans le menu tournois si vous voulez rejouer !"
                )

            else:
                self.get_tournament_players_instances(self.current_tournament)
                self.update_player_rank()
                self.generate_tournament_rounds()
                self.get_tournament_rounds_instances(self.current_tournament)

                for rounds, number_of_rounds in zip(
                    self.current_tournament.rounds,
                    range(len(self.current_tournament.rounds) + 1),
                ):
                    round_number = number_of_rounds + 1

                    self.start_rounds(rounds, round_number)

                    if round_number == 1:
                        self.play_first_round(rounds)
                    else:
                        self.play_next_round(rounds)

                    self.end_rounds(rounds, round_number)
                    self.update_player_rank()

                self.view.input_message(
                    "Fin du tournoi. Appuyez sur ENTRER pour revenir au menu"
                )

                self.get_tournament_players_ids(self.current_tournament)
                self.get_tournament_rounds_ids(self.current_tournament)

    def tournament_description(self):
        """show the current tournament description"""
        self.view.display_message(self.current_tournament.description)

        user_input = self.view.input_message(
            "[Entrer] : revenir au menu | [m] : modifier la description "
        )

        if user_input == "m":
            new_description = self.view.prompt_description(self.current_tournament)
            self.current_tournament.description = new_description
            self.current_tournament.update(
                "description", self.current_tournament.description
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

            return True

    def get_matches(self):
        """instantiate serialized matches and add them to the controller match dict"""
        matches = Match.load_matches()

        for match in matches:
            new_match = Match(
                player_one=match["player_one"],
                player_two=match["player_two"],
                m_id=match["m_id"],
            )
            new_match.player_one_score = match["player_one_score"]
            new_match.player_two_score = match["player_two_score"]

            self.matches_dict[new_match.m_id] = new_match

    def update_match_scores(self, match: Match):
        """update scores of match players

        Args:
            match (Match): current match
        """

        #  instantiate match's players from player id
        self.get_match_players_instances(match)

        #  Update players score in match instance
        match.player_one_score += self.view.prompt_player_score(match.player_one)
        match.player_two_score += self.view.prompt_player_score(match.player_two)

        #  Update players instances scores
        match.player_one.match_score += match.player_one_score
        match.player_two.match_score += match.player_two_score

        #  Update match data base
        match.update("player_one_score", match.player_one_score)
        match.update("player_two_score", match.player_two_score)

        # update player data
        match.player_one.update("match_score", match.player_one.match_score)
        match.player_two.update("match_score", match.player_two.match_score)

        self.get_match_players_ids(match)

    def get_match_players_instances(self, match: Match):
        """get players instances from the current tournament players dict

        Args:
            match (Match): current match
        """

        match.player_one = self.players_dict[match.player_one]
        match.player_two = self.players_dict[match.player_two]

    def get_match_players_ids(self, match: Match):
        """get players ids from Player.p_id

        Args:
            match (Match): current match
        """

        match.player_one = match.player_one.p_id
        match.player_two = match.player_two.p_id

    # Round functions
    def generate_tournament_rounds(self):
        """generates rounds for the current tournament based on the tournament's number of rounds"""
        tournament = self.current_tournament

        if tournament is not None:

            for rounds in range(int(tournament.number_of_rounds)):

                new_round_id = len(self.rounds_dict) + 1
                new_round = Round(f"Round {rounds + 1}", new_round_id)
                tournament.add_round(new_round.r_id)
                self.rounds_dict[new_round.r_id] = new_round

    def get_rounds(self):
        """instantiate serialized rounds and add them to the controller round dict"""
        rounds = Round.load_rounds()

        for new_rounds in rounds:
            new_round = Round(
                name=new_rounds["name"],
                r_id=new_rounds["r_id"],
            )
            new_round.list_of_matches = new_rounds["list_of_matches"]
            new_round.start_time = new_rounds["start_time"]
            new_round.end_time = new_rounds["end_time"]

            self.rounds_dict[new_round.r_id] = new_round

    def start_rounds(self, tournament_round: Round, round_number):
        """timestamps the start time of the current round

        Args:
            tournament_round (Round): current round
            round_number (_type_): number of the current round
        """
        self.view.display_message(f"TOUR {round_number}")

        self.view.input_message(
            f"Appuyer sur ENTRER pour commencer le tour {round_number}"
        )
        tournament_round.start_timestamp()

        self.view.display_message("------------------------------------------")
        self.view.display_message("Les joueurs suivant doivent s'affrontrer: ")
        self.view.display_message("------------------------------------------")
        sleep(0.5)

    def end_rounds(self, tournament_round, round_number):
        """timestamps the end time of the current round

        Args:
            tournament_round (Round): current round
            round_number (_type_): number of the current round
        """
        sleep(0.5)
        self.view.display_message("--------------")
        self.view.display_message(f"Fin du tour {round_number}")
        self.view.display_message("--------------")
        sleep(0.5)

        tournament_round.end_timestamp()

        self.view.display_message(f"début du tour: {tournament_round.start_time}")
        self.view.display_message(f"Fin du tour: {tournament_round.end_time}")
        sleep(0.4)

    def play_first_round(self, new_round: Round):
        """play the first round of the current tournament
        Args:
            new_round (Round): current round
        """
        pairs = self.first_round_pairs(self.current_tournament.players)

        for pair in pairs:
            self.new_match(pair[0], pair[1], new_round)
            self.view.display_message(f"{str(pair[0])} contre {str(pair[1])}")

        self.get_round_matches_instances(new_round)

        #  Start match and input players scores
        for matches in new_round.list_of_matches:

            match = matches

            self.view.display_message("------------------")
            self.view.display_message("Saisi des scores :")

            self.update_match_scores(match)

        self.get_round_matches_ids(new_round)

    def play_next_round(self, new_round):
        """play the current round of the current tournament
        Args:
            new_round (Round): current round
        """
        pairs = self.round_pairs(self.current_tournament.players)

        for pair in pairs:
            self.new_match(pair[0], pair[1], new_round)
            self.view.display_message(f"{str(pair[0])} contre {str(pair[1])}")

        self.get_round_matches_instances(new_round)

        #  Start match and input players scores
        for matches in new_round.list_of_matches:

            match = matches

            self.view.display_message("------------------")
            self.view.display_message("Saisi des scores :")

            self.update_match_scores(match)

        self.get_round_matches_ids(new_round)

    def get_round_matches_instances(self, current_round: Round):
        """converts matches ids into matches instances

        Args:
            current_round (Round): current round
        """
        current_round.list_of_matches = [
            self.matches_dict[matches] for matches in current_round.list_of_matches
        ]

    def get_round_matches_ids(self, current_round: Round):
        """converts matches instances back into matches ids

        Args:
            current_round (Round): current round
        """
        current_round.list_of_matches = [
            matches.m_id for matches in current_round.list_of_matches
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

    def menu_options(self):
        """Start and display the options menu : MENU OPTIONS"""
        menu_options = self.menu_view(
            "MENU OPTIONS",
            "Sauvegarder",
            "Charger",
            "Retour",
        )

        loop = True

        while loop:
            menu_choice = menu_options.start_menu()

            if menu_choice == 1:
                choice = self.view.input_message(
                    "Etes vous sur de vouloir sauvegarder les données ?"
                    "Les données précédement sauvegardé seront supprimées. (y: oui / n: non)"
                )
                if choice == "y":
                    self.erase_all_data()
                    self.save_all_data()

                    self.view.display_message("Les données ont bien été sauvegardé")

                elif choice == "n":
                    continue

                else:
                    self.view.display_message("Saisissez 'y' ou 'n' pour continuer")

            elif menu_choice == 2:
                choice = self.view.input_message(
                    "Etes vous sur de vouloir charger les données ? Les données actuelles seront supprimées."
                    "(y: oui / n: non)"
                )
                if choice == "y":
                    self.load_all_data()
                    self.get_players()
                    self.view.display_message("Les données ont bien été chargé")

                elif choice == "n":
                    continue
                else:
                    self.view.display_message("Saisissez 'y' ou 'n' pour continuer")

            elif menu_choice == 3:
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
        """starts and displays the players menu"""
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

    def menu_tournament_list(self):
        """starts and displays the tournament list menu"""

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

                    if self.current_tournament is not None:
                        self.menu_current_tournament()

                elif user_input >= len(self.tournament_dict):
                    loop = False

    def menu_current_tournament(self):
        """starts and displays the current tournament menu"""

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
        """starts and displays the tournament players menu"""
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
                self.get_tournament_players_instances(self.current_tournament)
                self.update_player_rank()
                self.get_tournament_players_ids(self.current_tournament)

            elif user_input == 4:
                loop = False

    def global_players_report(self):
        """displays the global players report"""
        if not self.players_dict:
            self.view.display_message("Il n'y a pas encore de joueurs de créé !")
        else:
            current_players = self.players_dict.values()
            info_players = defaultdict(list)

            for player in current_players:
                player_dict = player.display_player()
                for key, value in player_dict.items():
                    info_players[key].append(value)

            self.view.display_message(
                tabulate(info_players, headers="keys", tablefmt="grid")
            )
            self.view.input_message("Appuyer sur ENTRER pour revenir au menu")

    def tournaments_report(self):
        """displays tournaments reports"""
        if not self.tournament_dict:
            self.view.display_message("Il n'y a pas encore de tournoi de créé !")
        else:
            tournaments = self.tournament_dict.values()
            info_tournaments = defaultdict(list)

            for tournament in tournaments:
                tournament_dict = tournament.display_tournament()
                for key, value in tournament_dict.items():
                    info_tournaments[key].append(value)

            self.view.display_message(
                tabulate(info_tournaments, headers="keys", tablefmt="grid")
            )
            self.view.input_message("Appuyer sur ENTRER pour revenir au menu")

    def current_tournament_rounds_report(self):
        """displays rounds reports of the current tournament"""
        self.get_tournament_rounds_instances(self.current_tournament)

        if not self.current_tournament.rounds:
            self.view.display_message("Le tournoi n'a pas encore été joué !")
        else:
            tournament_rounds = self.current_tournament.rounds
            info_rounds = defaultdict(list)

            for tournament_round in tournament_rounds:
                round_dict = tournament_round.display_round()
                for key, value in round_dict.items():
                    info_rounds[key].append(value)

            self.view.display_message(
                tabulate(info_rounds, headers="keys", tablefmt="grid")
            )
            self.view.input_message("Appuyer sur ENTRER pour revenir au menu")

        self.get_tournament_rounds_ids(self.current_tournament)

    def current_tournament_matches_report(self):
        """displays matches reports from the current tournament"""
        self.get_tournament_players_instances(self.current_tournament)
        self.get_tournament_rounds_instances(self.current_tournament)
        for rounds in self.current_tournament.rounds:
            self.get_round_matches_instances(rounds)
            for matches in rounds.list_of_matches:
                self.get_match_players_instances(matches)

        if not self.current_tournament.rounds:
            self.view.display_message("Le tournoi n'a pas encore été joué !")
        else:
            info_matches = defaultdict(list)
            for rounds in self.current_tournament.rounds:

                for matches in rounds.list_of_matches:
                    match_dict = matches.display_match_result()
                    for key, value in match_dict.items():
                        info_matches[key].append(value)

            self.view.display_message(
                tabulate(info_matches, headers="keys", tablefmt="grid")
            )
            self.view.input_message("Appuyer sur ENTRER pour revenir au menu")

        for rounds in self.current_tournament.rounds:
            for matches in rounds.list_of_matches:
                self.get_match_players_ids(matches)

        for rounds in self.current_tournament.rounds:
            self.get_round_matches_ids(rounds)

        self.get_tournament_rounds_ids(self.current_tournament)
        self.get_tournament_players_ids(self.current_tournament)

    def current_tournament_players_report(self):
        """displays the players report of the current tournament"""
        self.get_tournament_players_instances(self.current_tournament)

        if not self.current_tournament.players:
            self.view.display_message("Il n'y a pas encore de joueurs d'inscrit !")
        else:
            current_players = self.current_tournament.players.values()
            info_players = defaultdict(list)

            for player in current_players:
                player_dict = player.display_player()
                for key, value in player_dict.items():
                    info_players[key].append(value)

            self.view.display_message(
                tabulate(info_players, headers="keys", tablefmt="grid")
            )
            self.view.input_message("Appuyer sur ENTRER pour revenir au menu")

        self.get_tournament_players_ids(self.current_tournament)

    def run(self):
        self.main_menu()
