class Tournament:
    def __init__(self, name, location, date, time_rule, max_number_player=8, rounds=4):

        self.players = []

        self.name = name
        self.location = location
        self.date = date
        self.time_rule = time_rule
        self.MAX_NUMBER_PLAYER = max_number_player
        self.rounds = rounds

    def add_player(self, player):
        self.players.append(player)
