from tinydb import TinyDB


match_db = TinyDB("saves/" + "match_db.json")


class Match:
    def __init__(self, player_one, player_two):
        """_summary_

        Args:
            player_one (_type_):instance of Player
            player_two (_type_):instance of Player
        """
        self.player_one = player_one
        self.player_two = player_two

        self.player_one_score = 0.0
        self.player_two_score = 0.0

        self.match = ([self.player_one, self.player_one_score], [self.player_two, self.player_two_score])

    def display_match_result(self):
        return {
            "Matchs": f"{self.player_one} contre {self.player_two}",
            "Résultats": f"{self.player_one_score} - {self.player_two_score}"
        }

    def save(self):
        serialized_match = {
            "Joueur 1": self.player_one,
            "Joueur 2": self.player_two,
            "Score J1": self.player_one_score,
            "Score J2": self.player_two_score
        }

        match_db.insert(serialized_match)

    def __str__(self):
        return f"{self.player_one} contre {self.player_two}"
