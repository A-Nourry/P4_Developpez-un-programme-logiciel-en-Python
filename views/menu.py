class Menu:
    def __init__(self, option_one, option_two=None, option_three=None):
        """_instantiate a Menu between 1 and 3 options. Must have a least one option._

        Args:
            option_one (_type_): _option 1 name_
            option_two (_type_, optional): _option 2 name_. Defaults to None.
            option_three (_type_, optional): _option 3 name_. Defaults to None.
        """
        self.menu_options = {
            1: option_one,
            2: option_two,
            3: option_three,
            4: "Exit",
        }

    def print_menu(self):
        for key in self.menu_options.keys():
            if key is not None:
                print(key, "--", self.menu_options[key])

    def option1(self):
        return 1

    def option2(self):
        return 2

    def option3(self):
        return 3

    def start_menu(self, menu_name):
        while True:

            # Menu name
            separators = "-" * len(menu_name)
            print(separators)
            print(menu_name)
            print(separators)

            self.print_menu()
            option = ""
            try:
                option = int(input("Enter your choice: "))
            except Menu.WrongInput:
                print("Wrong input. Please enter a number ...")
            # Check what choice was entered and act accordingly
            if option == 1:
                return option
            elif option == 2:
                self.option2()
            elif option == 3:
                self.option3()
            elif option == 4:
                print("Thanks message before exiting")
                exit()
            else:
                print("Invalid option. Please enter a number between 1 and 4.")


if __name__ == "__main__":
    menu = Menu("Nouveau tournoi", "Nouveau joueur", "Sauvegarder")
    menu_tournoi = Menu("ajouter un joueur")
    menu.start_menu("MENU PRINCIPAL")

    if menu.start_menu("MENU PRINCIPAL") == 1:
        menu_tournoi.start_menu("AJOUTER UN JOUEUR")
