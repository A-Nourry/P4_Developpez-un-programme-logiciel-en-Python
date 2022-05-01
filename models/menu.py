class Menu:
    def __init__(self, menu_title, *options):
        """_instantiate a Menu between 1 and 3 options. Must have a least one option._

        Args:
            option_one (_type_): _option 1 name_
            option_two (_type_, optional): _option 2 name_. Defaults to None.
            option_three (_type_, optional): _option 3 name_. Defaults to None.
        """
        self.menu_title = menu_title

        self.menu_options = {}
        key = 0
        for option in options:
            key += 1
            self.menu_options[key] = option

    def print_menu(self):
        separators = "-" * len(self.menu_title)
        print(separators)
        print(self.menu_title)
        print(separators)

        for key in self.menu_options.keys():
            print(key, "--", self.menu_options[key])

    def start_menu(self) -> int:
        while True:
            self.print_menu()
            option = ""
            try:
                option = int(input("Saisissez votre choix: "))
            except ValueError:
                print(
                    f"Wrong input. Please enter a number between 1 and {len(self.menu_options)}..."
                )
                continue

            if option == "":
                print("Merci d'avoir utilisé cette application !")
                exit()
            elif option > len(self.menu_options):
                print(
                    f"Invalid option. Please enter a number between 1 and {len(self.menu_options)}."
                )
            else:
                return option
