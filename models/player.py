from tinydb import TinyDB, Query


db = TinyDB("db.json")
players_table = db.table("players")
players = Query()


class Player:
    def __init__(
        self,
        first_name,
        last_name,
        birth_date,
        gender,
        rank: int = 1,
        p_id=0,
    ):
        """_summary_

        Args:
            first_name (str): first name of the player
            last_name (str): last name of the player
            birth_date (str): birthday of the player (xx/xx/xx)
            gender (str): gender of the player
            rank (int, optional): rank of the player. Defaults to 1.
            p_id (int, optional): ID of the player's object. Defaults to 0.
        """
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.gender = gender
        self.rank = rank
        self.p_id = p_id

        self.score = 0.0

    def display_player(self):
        return {
            "Prénom": self.first_name,
            "Nom": self.last_name,
            "Date de naissance": self.birth_date,
            "Sexe": self.gender,
            "Classement": self.rank,
            "Score": self.score,
        }

    def save(self):
        serialized_player = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "birth_date": self.birth_date,
            "gender": self.gender,
            "rank": self.rank,
            "score": self.score,
            "p_id": self.p_id,
        }

        players_table.insert(serialized_player)

    def load_players(self):
        players = []
        for player in players_table:
            players.append(player)

        return players

    def update(self, key, value):
        players_table.update({key: value}, players.p_id == self.p_id)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


def load_players():
    players = []
    for player in players_table:
        players.append(player)

    return players


def erase_player_data():
    players_table.truncate()
    return True
