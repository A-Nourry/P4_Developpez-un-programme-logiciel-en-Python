from tinydb import TinyDB, Query


db = TinyDB("db.json")
tournaments_table = db.table("tournaments")
tournaments = Query()


class Tournament:
    def __init__(
        self,
        name,
        location,
        date,
        time_rule,
        description,
        max_number_player=8,
        round_number=4,
        t_id=0,
    ):
        self.name = name
        self.location = location
        self.date = date
        self.time_rule = time_rule
        self.description = description
        self.MAX_NUMBER_PLAYER = max_number_player
        self.round_number = round_number
        self.t_id = t_id

        self.players = {}
        self.rounds = []

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
            "name": self.name,
            "location": self.location,
            "date": self.date,
            "time_rule": self.time_rule,
            "description": self.description,
            "max_number_player": self.MAX_NUMBER_PLAYER,
            "number_of_rounds": self.round_number,
            "t_id": self.t_id,
            "rounds": self.rounds,
            "players": self.players,
        }

        tournaments_table.insert(serialized_tournament)

    def update(self, key, value, tournament_id):

        tournaments_table.update({key: value}, tournaments.t_id == tournament_id)

    def add_player_id_to_dict(self, player_number, player_id, tournament_id):
        self.players[player_number] = player_id

        self.update("players", self.players, tournament_id)

    def add_round(self, new_round_id, tournament_id):
        self.rounds.append(new_round_id)

        self.update("rounds", self.rounds, tournament_id)

    def __repr__(self):
        return f"{self.name}"


def load_tournaments():
    serialized_tournaments = []
    for tournaments in tournaments_table:
        serialized_tournaments.append(tournaments)

    return serialized_tournaments
