from models.player import Player
from models.tournament import Tournament


class Controller:
    def __init__(self, view):

        # views
        self.view = view

    def add_player(self, tournament: Tournament):
        if tournament is not None:
            new_player = self.view.prompt_new_player()

            player = Player(
                first_name=new_player["first_name"],
                last_name=new_player["last_name"],
                birth_date=new_player["birth_date"],
                gender=new_player["gender"],
                rank=new_player["rank"],
            )

            tournament.add_player(player)

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

    def run(self):
        print("NOUVEAU TOURNOI")
        tournament = self.new_tournament()

        print("AJOUT DES JOUEURS")
        for _ in range(tournament.MAX_NUMBER_PLAYER):
            self.add_player(tournament)

        print(tournament.players)
