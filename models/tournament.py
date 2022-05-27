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
        number_of_rounds=4,
        t_id=0,
    ):
        """Tournament instance attributes

        Args:
            name (str): name of the tournament
            location (str): location of the tournament
            date (str): date of the tournament (xx/xx/xx)
            time_rule (str): rule of the tournament (blitz, bullet or speed)
            description (str): description of the tournament
            max_number_player (int, optional): _description_. Defaults to 8.
            number_of_rounds (int, optional): _description_. Defaults to 4.
            t_id (int, optional): _description_. Defaults to 0.
        """
        self.name = name
        self.location = location
        self.date = date
        self.time_rule = time_rule
        self.description = description
        self.MAX_NUMBER_PLAYER = max_number_player
        self.number_of_rounds = number_of_rounds
        self.t_id = t_id

        self.players = {}
        self.rounds = []

    def display_tournament(self):
        """display Tournament's attributes

        Returns:
            dict: returns a dict of the Tournament's attributes
        """
        return {
            "Nom": self.name,
            "Lieu": self.location,
            "Date": self.date,
            "Règle du temps": self.time_rule,
            "Nombre de joueurs": self.MAX_NUMBER_PLAYER,
            "Nombre de tours": self.number_of_rounds,
        }

    def save(self):
        """save Tournament attributes in the data base"""
        serialized_tournament = {
            "name": self.name,
            "location": self.location,
            "date": self.date,
            "time_rule": self.time_rule,
            "description": self.description,
            "max_number_player": self.MAX_NUMBER_PLAYER,
            "number_of_rounds": self.number_of_rounds,
            "t_id": self.t_id,
            "rounds": self.rounds,
            "players": self.players,
        }

        tournaments_table.insert(serialized_tournament)

    def update(self, key, value):
        """update Tournament attributes of the data base

        Args:
            key (str): key of the data base's dict
            value (_type_): value of the data base's dict
        """
        tournaments_table.update({key: value}, tournaments.t_id == self.t_id)

    def add_player_id_to_dict(self, player_number, player_id):
        """add a player id to the Tournament's dict (self.players)

        Args:
            player_number (str): number of the player
            player_id (int): id of a Player instance (Player.p_id)
        """
        self.players[player_number] = player_id

        self.update("players", self.players)

    def add_round(self, new_round_id):
        """add a round to the round list (self.rounds)

        Args:
            new_round_id (int): round id from a Round instance (Round.r_id)
        """
        self.rounds.append(new_round_id)

        self.update("rounds", self.rounds)

    def __repr__(self):
        return f"{self.name}"


def load_tournaments():
    """get Tournament attributes from the data base

    Returns:
        dict: return a list of dicts, of all Tournament instances attributes
    """
    serialized_tournaments = []
    for tournaments in tournaments_table:
        serialized_tournaments.append(tournaments)

    return serialized_tournaments
