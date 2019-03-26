import tcod as libtcod
import tcod.event
import tcod.console

from input_handlers import handle_keys
from entity import Entity
from fov_functions import initialize_fov, recompute_fov
from map_objects.game_map import GameMap
from render_functions import clear_all, render_all


def main():
    screen_width = 80
    screen_height = 60
    map_width = 80
    map_height = 45

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 10
    # panel_height = int(screen_height / 2)

    colors = {
        'dark_wall': libtcod.Color(0, 0, 100),
        'dark_ground': libtcod.Color(50, 50, 150),
        'light_wall': libtcod.Color(130, 110, 50),
        'light_ground': libtcod.Color(200, 180, 50)
    }

    player = Entity(int(screen_width / 2), int(screen_height / 2), '@', libtcod.white)
    npc = Entity(int(screen_width / 2) - 5, int(screen_height / 2), '@', libtcod.yellow)
    entities = [player, npc]

    libtcod.console_set_custom_font("img/terminal12x12_gs_ro.png",
                                    libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_CP437)
    libtcod.sys_set_fps(60)
    root = libtcod.console_init_root(screen_width, screen_height, 'PyRL', False, renderer=libtcod.RENDERER_SDL2)
    con = libtcod.console.Console(screen_width, screen_height)
    # panel = libtcod.console.Console(screen_width, panel_height)

    # root.print(screen_width // 2 - 7, screen_height // 2 - 12, 'RogueSouls', fg=libtcod.crimson,
    #            bg=libtcod.darkest_han)
    # root.print(screen_width // 2 - 8, screen_height // 2 - 10, 'By Jerezereh')

    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player)

    fov_recompute = True
    fov_map = initialize_fov(game_map)

    while True:
        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)
        render_all(con, root, entities, game_map, fov_map, fov_recompute,  screen_width, screen_height, colors)
        fov_recompute = False
        libtcod.console_flush()
        clear_all(con, entities)

        for event in libtcod.event.get():
            if event.type == "QUIT":
                return True
            if event.type == "KEYDOWN":
                action = handle_keys(event)
            else:
                action = None

            if action is not None:
                move = action.get('move')
                exit = action.get('exit')
                fullscreen = action.get('fullscreen')

                if move:
                    dx, dy = move
                    if not game_map.is_blocked(player.x + dx, player.y + dy):
                        player.move(dx, dy)
                        fov_recompute = True

                if exit:
                    return True

                if fullscreen:
                    libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())


if __name__ == "__main__":
    main()
