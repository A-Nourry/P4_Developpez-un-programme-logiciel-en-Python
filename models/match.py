class Match:
    def __init__(self, player_one, player_two):
        """_summary_

        Args:
            player_one (_type_):instance of Player
            player_two (_type_):instance of Player
        """
        self.player_one = player_one
        self.player_two = player_two

    def play_match(self):
        player_one_result = input(f"Score de {self.player_one}: ")
        player_two_result = input(f"Score de {self.player_two}: ")
        return player_one_result, player_two_result

    def __str__(self):
        return f"{self.player_one} affronte {self.player_two}"
