import tcod as libtcod
import tcod.event


def handle_keys(key):
    # Movement keys
    if key.sym == libtcod.event.K_UP:
        return {'move': (0, -1)}
    elif key.sym == libtcod.event.K_DOWN:
        return {'move': (0, 1)}
    elif key.sym == libtcod.event.K_LEFT:
        return {'move': (-1, 0)}
    elif key.sym == libtcod.event.K_RIGHT:
        return {'move': (1, 0)}

    if key.sym == libtcod.event.K_RETURN and key.mod == libtcod.event.KMOD_ALT:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}

    elif key.sym == libtcod.event.K_ESCAPE:
        # Exit the game
        return {'exit': True}

    # No key was pressed
    return {}
