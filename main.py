from controllers.base import Controller
from views.base import UserView
from views.menu import Menu


def main():
    # Views
    view = UserView
    menu = Menu

    # Controller
    game = Controller(view, menu)

    game.run()


if __name__ == "__main__":
    main()
