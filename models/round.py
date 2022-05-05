from datetime import datetime, date


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
        return {"Matchs": self.list_of_matches}
