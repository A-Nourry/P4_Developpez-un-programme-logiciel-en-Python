from tinydb import TinyDB, Query


db = TinyDB("db.json")
matches_table = db.table("matches")
matches = Query()


class Match:
    def __init__(self, player_one, player_two, m_id):
        """Match instance attributes

        Args:
            player_one (instance):instance of Player
            player_two (instance):instance of Player
        """
        self.player_one = player_one
        self.player_two = player_two
        self.m_id = m_id

        self.player_one_score = 0.0
        self.player_two_score = 0.0

        self.match_result = (
            [self.player_one, self.player_one_score],
            [self.player_two, self.player_two_score],
        )

    def display_match_result(self):
        """display match results in a dict"""
        return {
            "Matchs": f"{self.player_one} contre {self.player_two}",
            "Résultats": f"{self.player_one_score} - {self.player_two_score}",
        }

    def save(self):
        """save Match attributes in the data base"""
        serialized_match = {
            "player_one": self.player_one,
            "player_two": self.player_two,
            "m_id": self.m_id,
            "player_one_score": self.player_one_score,
            "player_two_score": self.player_two_score,
        }

        matches_table.insert(serialized_match)

    def update(self, key, value):
        """update Match attributes in the data base

        Args:
            key (str): key of the data base's dict
            value (_type_): value of the data base's dict
        """
        matches_table.update({key: value}, matches.m_id == self.m_id)

    def __str__(self):
        return f"{self.player_one} contre {self.player_two}"

    @staticmethod
    def load_matches():
        """get Match attributes from the data base and return them

        Returns:
            dict: dict of attributes
        """
        serialized_matches = []
        for matches in matches_table:
            serialized_matches.append(matches)

        return serialized_matches

    @staticmethod
    def erase_data():
        matches_table.truncate()
