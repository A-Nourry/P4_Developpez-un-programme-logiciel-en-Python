from tinydb import TinyDB


tournament_db = TinyDB("saves/tournament_db.json")


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

    def display_tournament(self):
        return {
            "Nom": self.name,
            "Lieu": self.location,
            "Date": self.date,
            "Règle du temps": self.time_rule,
            "Nombre de joueurs": self.MAX_NUMBER_PLAYER,
            "Nombre de tours": self.round_number,
        }

    def save(self):
        serialized_tournament = {
            "Nom": self.name,
            "Lieu": self.location,
            "Date": self.date,
            "Règle du temps": self.time_rule,
            "Nombre de joueurs": self.MAX_NUMBER_PLAYER,
            "Nombre de tours": self.round_number,
            "Description": self.description,
            "Tours": self.rounds,
            "Joueurs": self.players,
        }

        tournament_db.insert(serialized_tournament)

    def add_player_to_dict(self, player_number, player):
        self.players[player_number] = player

    def add_round(self, rounds):
        self.rounds.append(rounds)

    def __repr__(self):
        return f"{self.name}"


def load_tournaments():
    serialized_tournaments = []
    for tournaments in tournament_db:
        serialized_tournaments.append(tournaments)

    return serialized_tournaments
