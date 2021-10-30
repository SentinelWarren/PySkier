#!/usr/bin/env python3

from pyskier.game import SkierGame


if __name__ == '__main__':

    # Play the game
    skier_game = SkierGame('images/')
    skier_game.run()
    skier_game.quit()