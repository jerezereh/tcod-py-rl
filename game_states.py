from enum import Enum


class GameStates(Enum):
    PLAYER_TURN = 1
    ENEMY_TURN = 2
    PLAYER_DEAD = 3
    # MENU_SCREEN = 4
    SHOW_INVENTORY = 4
    DROP_INVENTORY = 5
    # TARGETING = 5
    LEVEL_UP = 6
    CHARACTER_SCREEN = 7
