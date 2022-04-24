from controllers.base import Controller
from views.base import UserView


def main():
    view = UserView
    game = Controller(view)
    game.run()


if __name__ == "__main__":
    main()
