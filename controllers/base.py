from models.player import Player

# from models.tournament import Tournament


class Controller:
    def __init__(self, view):

        # views
        self.view = view

        self.player_list = []

    def add_player(self):
        new_player = self.view.prompt_new_player()

        player = Player(
            new_player[0], new_player[1], new_player[2], new_player[3], new_player[4]
        )
        self.player_list.append(player)

    def run(self):
        self.add_player()
        print(str(self.player_list))
