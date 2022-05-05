class Player:
    def __init__(self, first_name, last_name, birth_date, gender, rank: int = 1):
        """_summary_

        Args:
            first_name (_type_): prénom du joueur
            last_name (_type_): nom du joueur
            birth_date (_type_): date de naissance, format : xx/xx/xx
            gender (_type_): Sexe du joueur
            rank (int): Classement du joueur
        """
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.gender = gender
        self.rank = rank

    def display_player(self):
        return {
            "Prénom": self.first_name,
            "Nom": self.last_name,
            "Date de naissance": self.birth_date,
            "Sexe": self.gender,
            "Classement": self.rank,
        }

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
