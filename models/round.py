class Round:
    def __init__(self, name, start_times, end_times):
        """_summary_

        Args:
            name (_type_): name of the round
            start_times (_type_): starting round date, format : xx/xx/xx à xx:xx
            end_times (_type_): ending round date, format : xx/xx/xx à xx:xx
        """

        self.list_of_matches = []

        self.name = name
        self.start_times = start_times
        self.end_times = end_times

    def add_match_to_list(self, match):
        self.list_of_matches.append(match)
