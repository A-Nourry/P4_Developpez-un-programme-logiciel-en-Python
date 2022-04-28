from models.player import Player
from models.tournament import Tournament
from models.match import Match
from models.round import Round


class Controller:
    def __init__(self, view):

        # views
        self.view = view

    def add_player(self, tournament: Tournament):
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

            tournament.add_player_to_dict(player)

            return True

    def new_tournament(self):
        new_tournament = self.view.prompt_for_tournament()

        tournament = Tournament(
            name=new_tournament["name"],
            location=new_tournament["location"],
            date=new_tournament["date"],
            time_rule=new_tournament["rule"],
            rounds=new_tournament["round"],
        )
        return tournament

    def generate_pairs(self, player_dict):
        """generate pairs of players from a dict"""

        first_pair = (player_dict["Joueur 1"], player_dict["Joueur 2"])
        second_pair = (player_dict["Joueur 3"], player_dict["Joueur 4"])
        third_pair = (player_dict["Joueur 5"], player_dict["Joueur 6"])
        fourth_pair = (player_dict["Joueur 7"], player_dict["Joueur 8"])

        return first_pair, second_pair, third_pair, fourth_pair

    def add_match(self, pair_of_players, match_round: Round):
        """instantiate Match object and add it to the list of matches from Round object"""

        if match_round is not None:
            match = Match(pair_of_players[0], pair_of_players[1])
            match_round.add_match_to_list(match)

            return True

    def new_round(self, round_number):
        """instantiate Round object and return it"""

        new_round = Round(f"Round + {round_number}", "start_time", "end_time")
        return new_round

    def run(self):
        # Tournament creation
        print("NOUVEAU TOURNOI")
        tournament = self.new_tournament()

        # Players creation
        print(f"AJOUT DES {tournament.MAX_NUMBER_PLAYER} JOUEURS")
        for i in range(tournament.MAX_NUMBER_PLAYER):
            print("JOUEUR", i + 1)
            self.add_player(tournament)

        # Rounds
        for rounds in tournament.rounds:
            print(f"TOUR {rounds}")
            new_round = self.new_round(f"TOUR {rounds}")
            print(f"génération des paires de joueurs pour le tour {rounds}...")
            pairs = self.generate_pairs(tournament.players)
            print(pairs)

            print("génération des matchs...")
            for pair in pairs:
                self.add_match(pair, new_round)

            for matches in new_round.list_of_matches:
                print(matches)
                match = matches
                match.play_match()
