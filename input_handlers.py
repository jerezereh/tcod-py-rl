import tcod as libtcod
import tcod.event

from game_states import GameStates


def handle_keys(key, game_state):
    if game_state == GameStates.PLAYER_TURN:
        return handle_player_turn_keys(key)
    elif game_state == GameStates.PLAYER_DEAD:
        return handle_player_dead_keys(key)
    elif game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        return handle_inventory_keys(key)

    return {}


def handle_player_turn_keys(key):
    # Movement keys
    if key.sym == libtcod.event.K_UP or key.sym == libtcod.event.K_w:
        return {'move': (0, -1)}
    elif key.sym == libtcod.event.K_DOWN or key.sym == libtcod.event.K_s:
        return {'move': (0, 1)}
    elif key.sym == libtcod.event.K_LEFT or key.sym == libtcod.event.K_a:
        return {'move': (-1, 0)}
    elif key.sym == libtcod.event.K_RIGHT or key.sym == libtcod.event.K_d:
        return {'move': (1, 0)}
    elif key.sym == libtcod.event.K_q:
        return {'move': (-1, -1)}
    elif key.sym == libtcod.event.K_e:
        return {'move': (1, -1)}
    elif key.sym == libtcod.event.K_z:
        return {'move': (-1, 1)}
    elif key.sym == libtcod.event.K_c:
        return {'move': (1, 1)}
    elif key.sym == libtcod.event.K_g:
        return {'pickup': True}
    elif key.sym == libtcod.event.K_i:
        return {'show_inventory': True}
    elif key.sym == libtcod.event.K_p:
        return {'drop_inventory': True}
    elif key.sym == libtcod.event.K_RETURN and key.mod == libtcod.event.KMOD_ALT:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}
    elif key.sym == libtcod.event.K_ESCAPE:
        # Exit the game
        return {'exit': True}

    # No known key was pressed
    print(key)
    return {}


def handle_player_dead_keys(key):
    if key.sym == libtcod.event.K_i:
        return {'show_inventory': True}
    elif key.sym == libtcod.event.K_RETURN and key.mod == libtcod.event.KMOD_ALT:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}
    elif key.sym == libtcod.event.K_ESCAPE:
        # Exit the game
        return {'exit': True}

    return {}


def handle_inventory_keys(key):
    index = key.sym - ord('a')

    if index >= 0:
        return {'inventory_index': index}
    elif key.sym == libtcod.event.K_RETURN and key.mod == libtcod.event.KMOD_ALT:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}
    elif key.sym == libtcod.event.K_ESCAPE:
        # Exit the menu
        return {'exit': True}

    return {}
