import tcod as libtcod
import tcod.event
import tcod.console

from input_handlers import handle_keys
from entity import Entity, get_blocking_entities_at_location
from fov_functions import initialize_fov, recompute_fov
from game_states import GameStates
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

    max_monsters_per_room = 3

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

    player = Entity(0, 0, '@', libtcod.white, 'Player', True)
    entities = [player]

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
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities,
                      max_monsters_per_room)

    fov_recompute = True
    fov_map = initialize_fov(game_map)

    game_state = GameStates.PLAYER_TURN

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

                if move and game_state == GameStates.PLAYER_TURN:
                    dx, dy = move
                    destination_x = player.x + dx
                    destination_y = player.y + dy
                    if not game_map.is_blocked(destination_x, destination_y):
                        target = get_blocking_entities_at_location(entities, destination_x, destination_y)

                        if target:
                            print('You kick the ' + target.name + ' in the shins, much to its annoyance!')
                        else:
                            player.move(dx, dy)
                            fov_recompute = True
                        game_state = GameStates.ENEMY_TURN

                if exit:
                    return True

                if fullscreen:
                    libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

                if game_state == GameStates.ENEMY_TURN:
                    for entity in entities:
                        if entity != player:
                            print('The ' + entity.name + ' ponders the meaning of its existence.')

                    game_state = GameStates.PLAYER_TURN


if __name__ == "__main__":
    main()
