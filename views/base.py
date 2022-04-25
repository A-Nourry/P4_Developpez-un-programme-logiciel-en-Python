class UserView:
    def prompt_new_player():
        first_name = input("Prénom du joueur: ")
        last_name = input("Nom du joueur: ")
        birth_date = input("Date de naissance: ")
        gender = input("homme ou femme ? ")
        rank = input("classement ? ")
        return {
            "first_name": first_name,
            "last_name": last_name,
            "birth_date": birth_date,
            "gender": gender,
            "rank": rank,
        }

    def prompt_for_tournament():
        tournament_name = input("Nom du tournoi: ")
        tournament_location = input("Lieu du tournoi: ")
        tournament_date = input("Date du tournoi: ")
        tournament_rule = input("règle du tournoi ? (bullet, blitz ou speed) ")
        tournament_rounds = input("Nombre de tours: ")
        return {
            "name": tournament_name,
            "location": tournament_location,
            "date": tournament_date,
            "rule": tournament_rule,
            "round": tournament_rounds,
        }
