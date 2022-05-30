class Menu:
    def __init__(self, menu_title, *options):
        """_instantiate a menu with an undefined number of options. Must have at least one option._

        Args:
            menu_title (str): _put the menu title here_
        """
        self.menu_title = menu_title

        self.menu_options = {}
        key = 0
        for option in options:
            key += 1
            self.menu_options[key] = option

    def print_menu(self):
        """displays the menu
        """
        separators = "-" * len(self.menu_title)
        print(separators)
        print(self.menu_title)
        print(separators)

        for key, value in self.menu_options.items():
            print(f"[{key}] {value}")

    def start_menu(self) -> int:
        """get an input from the user and returns it

        Returns:
            int: user input
        """
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
            if option > len(self.menu_options):
                print(
                    f"Invalid option. Please enter a number between 1 and {len(self.menu_options)}."
                )
            else:
                return option
