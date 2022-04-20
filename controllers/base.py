from models.player import Player


class Controller:

    def __init__(self):

        self.player_list = []

    def add_player(self):
        first_name = input("Prénom du joueur: ")
        last_name = input("Nom du joueur: ")
        birth_date = input("Date de naissance: ")
        sex = input("homme ou femme ? ")
        rank = input("classement ? ")

        player = Player(first_name, last_name, birth_date, sex, rank)
        self.player_list.append(player)

    def run(self):
        self.add_player()
        print(str(self.player_list))
