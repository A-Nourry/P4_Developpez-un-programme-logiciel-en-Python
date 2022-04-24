class Tournament:
    def __init__(self, name, location, date, time_rule, rounds=4):
        self.name = name
        self.location = location
        self.date = date
        self.time_rule = time_rule
        self.rounds = rounds

    def PlayerList(self, players):
        list_of_players = []
        list_of_players.append(players)
        return list_of_players


tournoi = Tournament("tournoi", "alsace", "10/10/10", "blitz", 4)
test = tournoi.PlayerList("test")
print(test)
