class UserView:
    def prompt_new_player():
        first_name = input("Prénom du joueur: ")
        last_name = input("Nom du joueur: ")
        birth_date = input("Date de naissance: ")
        gender = input("homme ou femme ? ")
        rank = input("classement ? ")
        return first_name, last_name, birth_date, gender, rank

    def prompt_for_tournament():
        tournament_name = input("Nom du tournoi: ")
        tournament_location = input("Lieu du tournoi: ")
        tournament_date = input("Date du tournoi: ")
        tournament_rule = input("règle du tournoi ? (bullet, blitz ou speed) ")
        tournament_rounds = input("Nombre de tours: ")
        return tournament_name, tournament_location, tournament_date, tournament_rule, tournament_rounds
