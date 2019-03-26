import tcod as libtcod
import tcod.event


def handle_keys(key):
    # Movement keys
    if key.sym == libtcod.event.K_UP or key.sym == libtcod.event.K_i:
        return {'move': (0, -1)}
    elif key.sym == libtcod.event.K_DOWN or key.sym == libtcod.event.K_k:
        return {'move': (0, 1)}
    elif key.sym == libtcod.event.K_LEFT or key.sym == libtcod.event.K_j:
        return {'move': (-1, 0)}
    elif key.sym == libtcod.event.K_RIGHT or key.sym == libtcod.event.K_l:
        return {'move': (1, 0)}
    elif key.sym == libtcod.event.K_u:
        return {'move': (-1, -1)}
    elif key.sym == libtcod.event.K_o:
        return {'move': (1, -1)}
    elif key.sym == libtcod.event.K_n:
        return {'move': (-1, 1)}
    elif key.sym == libtcod.event.K_PERIOD:
        return {'move': (1, 1)}

    if key.sym == libtcod.event.K_RETURN and key.mod == libtcod.event.KMOD_ALT:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}

    elif key.sym == libtcod.event.K_ESCAPE:
        # Exit the game
        return {'exit': True}

    # No known key was pressed
    return {}
