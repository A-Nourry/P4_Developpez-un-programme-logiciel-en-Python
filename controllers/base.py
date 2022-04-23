from models.player import Player


class Controller:
    def __init__(self, view):

        # views
        self.view = view

        self.player_list = []

    def add_player(self):
        first_name = self.view.prompt_first_name()
        last_name = self.view.prompt_last_name()
        birth_date = self.view.prompt_birth_date()
        gender = self.view.prompt_gender()
        rank = self.view.prompt_rank()

        player = Player(first_name, last_name, birth_date, gender, rank)
        self.player_list.append(player)

    def run(self):
        self.add_player()
        print(str(self.player_list))
