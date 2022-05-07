class UserView:
    def prompt_new_player():
        first_name = input("Prénom du joueur: ")
        last_name = input("Nom du joueur: ")
        birth_date = input("Date de naissance: ")
        gender = input("homme ou femme ? ")

        while True:  # Rank value must be between 1 and 8
            try:
                rank = int(input("classement ? "))
                if not 1 <= rank <= 8:
                    raise ValueError()
                break
            except ValueError:
                print("Attention ! Vous devez saisir un entier entre 1 et 8 !")

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

        while True:  # tournament_rounds must be an integer > 0
            try:
                tournament_rounds = int(input("Nombre de tours: "))
                if tournament_rounds == 0:
                    raise ValueError()
                break
            except ValueError:
                print("Attention ! Vous devez saisir un entier supérieur à 1 !")

        return {
            "name": tournament_name,
            "location": tournament_location,
            "date": tournament_date,
            "rule": tournament_rule,
            "round": tournament_rounds,
        }

    def prompt_player_score(match_player):
        player_score = ""

        while True:
            try:
                player_score = float(input(f"Score de {match_player}: "))
                if player_score > 1:
                    raise ValueError()
                break
            except ValueError:
                print(
                    "Vous devez saisir l'un de ces scores : 1 pour le gagnant, 0 pour le perdant, 0.5 si match nul"
                )

        return player_score

    def prompt_player_rank():

        rank = ""

        while True:  # Rank value must be between 1 and 8
            try:
                rank = int(input("Veuillez saisir le nouveau classement du joueur: "))
                if not 1 <= rank <= 8:
                    raise ValueError()
                break
            except ValueError:
                print("Attention ! Vous devez saisir un entier entre 1 et 8 !")

        return rank

    def prompt_description(tournament):
        print("------------------------")
        print("Description du tournoi: ")
        tournament_description = input(tournament.description)
        print("------------------------")
        input("Appuyer sur ENTRER pour valider")
        return tournament_description
