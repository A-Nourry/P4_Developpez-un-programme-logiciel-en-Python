from datetime import datetime, date
from tinydb import TinyDB


db = TinyDB("db.json")
rounds_table = db.table("rounds")


class Round:
    def __init__(self, name):
        self.list_of_matches = []

        self.name = name
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

    def add_match_to_list(self, match):
        self.list_of_matches.append(match)

    def display_round(self):
        return {
            "Nom": self.name,
            "Début": self.start_time,
            "Fin": self.end_time,
        }

    def save(self):
        serialized_round = {
            "name": self.name,
            "start_time": self.start_time,
            "end_time": self.end_time,
        }

        rounds_table.insert(serialized_round)

    def __str__(self):
        return self.name


def load_rounds():
    serialized_rounds = []
    for rounds in rounds_table:
        serialized_rounds.append(rounds)

    return serialized_rounds
