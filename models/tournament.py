class Tournament:
    def __init__(self, name, location, date, time_rule, max_number_player=8, rounds=4):

        self.players = {}
        self.rounds = []

        self.name = name
        self.location = location
        self.date = date
        self.time_rule = time_rule
        self.MAX_NUMBER_PLAYER = max_number_player
        self.rounds = rounds

    def add_player_to_dict(self, player):

        for i in range(self.MAX_NUMBER_PLAYER):

            self.players[f"Joueur {i + 1}"] = player

    def add_round(self, round):
        self.rounds.append(round)
