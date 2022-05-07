class Match:
    def __init__(self, player_one, player_two):
        """_summary_

        Args:
            player_one (_type_):instance of Player
            player_two (_type_):instance of Player
        """
        self.player_one = player_one
        self.player_two = player_two

        self.player_one_result = None
        self.player_two_result = None

        self.match = ([self.player_one, self.player_one_result], [self.player_two, self.player_two_result])

    def display_match_result(self):
        return {
            self.player_one: self.player_one_result,
            self.player_two: self.player_two_result
        }

    def __str__(self):
        return f"{self.player_one} contre {self.player_two}"
