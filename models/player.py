class Player:
    def __init__(self, first_name, last_name, birth_date, sex, rank=int):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.sex = sex
        self.rank = rank

    def __str__(self):
        return f"{self.first_name} {self.last_name}, {self.sex}, né(e) le {self.birth_date} de rang {self.rank}"


"""class PlayerList(list):
    def append(self, object):

        if not isinstance(object, Player):
            return ValueError("Vous ne pouvez ajouter que des joueurs !")
        return super().append(object)"""
