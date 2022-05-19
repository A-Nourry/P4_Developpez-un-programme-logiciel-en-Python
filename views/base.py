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
        tournament_description = input("Description du tournoi: ")

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
            "description": tournament_description,
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

    def prompt_player_rank(player):

        rank = ""

        while True:  # Rank value must be between 1 and 8
            try:
                rank = int(
                    input(f"Veuillez saisir le nouveau classement de {player} : ")
                )
                if not 1 <= rank <= 8:
                    raise ValueError()
                break
            except ValueError:
                print("Attention ! Vous devez saisir un entier entre 1 et 8 !")

        return rank

    def prompt_description(tournament):
        print("------------------------")
        print("Description du tournoi: ")
        print(tournament.description)
        tournament_description = input()
        print("------------------------")
        input("Appuyer sur ENTRER pour valider")
        return tournament_description

    def prompt_warning_number_players(max_number_players, tournament_players):
        print("Attention : ")
        print(
            f"Pour inscrire des joueurs à ce tournoi, vous devez avoir créé au minimum {max_number_players} "
            f"joueurs dans le menu principal avant de continuer ! "
            f"({len(tournament_players)}/{max_number_players})"
        )
        print("")
        input("Appuyer sur ENTRER pour retourner au menu")

    def display_message(message):
        print(message)

    def input_message(message):
        user_input = input(message)
        return user_input
