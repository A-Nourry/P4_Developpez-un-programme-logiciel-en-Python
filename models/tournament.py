class Tournament:
    def __init__(
        self, name, location, date, time_rule, max_number_player=8, round_number=4
    ):

        self.players = {}
        self.rounds = []
        self.description = ""

        self.name = name
        self.location = location
        self.date = date
        self.time_rule = time_rule
        self.MAX_NUMBER_PLAYER = max_number_player
        self.round_number = round_number

    def add_player_to_dict(self, player_number, player):
        self.players[player_number] = player

    def add_round(self, rounds):
        self.rounds.append(rounds)

    def __repr__(self):
        return f"{self.name}"
