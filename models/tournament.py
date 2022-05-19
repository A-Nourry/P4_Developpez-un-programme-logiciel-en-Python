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

        self.players = {}
        self.rounds = []

        self.name = name
        self.location = location
        self.date = date
        self.time_rule = time_rule
        self.description = description
        self.MAX_NUMBER_PLAYER = max_number_player
        self.round_number = round_number
        self.t_id = t_id

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

    def add_player_id_to_dict(self, player_number, player_id, tournament_id):
        self.players[player_number] = player_id

        tournaments_table.update(
            {"players": self.players}, tournaments.t_id == tournament_id
        )

    def add_round(self, rounds):
        self.rounds.append(rounds)

    def __repr__(self):
        return f"{self.name}"


def load_tournaments():
    serialized_tournaments = []
    for tournaments in tournaments_table:
        serialized_tournaments.append(tournaments)

    return serialized_tournaments
