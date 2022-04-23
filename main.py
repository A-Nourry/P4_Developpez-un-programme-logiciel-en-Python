from controllers.base import Controller
from views.player import PlayerView


def main():
    view = PlayerView
    game = Controller(view)
    game.run()


if __name__ == "__main__":
    main()
