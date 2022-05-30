from datetime import datetime, date
from tinydb import TinyDB, Query


db = TinyDB("db.json")
rounds_table = db.table("rounds")
rounds = Query()


class Round:
    def __init__(self, name, r_id):
        """round instance attributes

        Args:
            name (str): name of the round
            r_id (int): id of the round
        """
        self.name = name
        self.r_id = r_id

        self.list_of_matches = []

        self.start_time = ""
        self.end_time = ""

    def start_timestamp(self):
        """returns current time"""
        now = datetime.now()
        today = date.today()

        current_date = today.strftime("%d/%m/%Y")
        current_time = now.strftime("%H:%M")

        time = f"{current_date} à {current_time}"

        self.start_time = time

    def end_timestamp(self):
        """returns current time"""
        now = datetime.now()
        today = date.today()

        current_date = today.strftime("%d/%m/%Y")
        current_time = now.strftime("%H:%M")

        time = f"{current_date} à {current_time}"

        self.end_time = time

    def add_match_to_list(self, match_id, round_id):
        """add a Match instance to the list of matches

        Args:
            match_id (int): id of a Match instance
            round_id (int): id of a Round instance
        """
        self.list_of_matches.append(match_id)

        self.update("list_of_matches", self.list_of_matches, round_id)

    def display_round(self):
        """display round attributes

        Returns:
            dict: returns a dict of the round attributes
        """
        return {
            "Nom": self.name,
            "Début": self.start_time,
            "Fin": self.end_time,
        }

    def save(self):
        """save round attributes in the data base"""
        serialized_round = {
            "name": self.name,
            "r_id": self.r_id,
            "list_of_matches": self.list_of_matches,
            "start_time": self.start_time,
            "end_time": self.end_time,
        }

        rounds_table.insert(serialized_round)

    def update(self, key, value, round_id):
        """update round attributes of the data base

        Args:
            key (str): key of the data base's dict
            value (_type_): value of the data base's dict
            round_id (int): id of the round (round.r_id)
        """
        rounds_table.update({key: value}, rounds.r_id == round_id)

    def __str__(self):
        return self.name

    @staticmethod
    def load_rounds():
        """get round attributes from the data base

        Returns:
            dict: returns a dict of rounds attributes
        """
        serialized_rounds = []
        for rounds in rounds_table:
            serialized_rounds.append(rounds)

        return serialized_rounds
