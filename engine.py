import tcod as libtcod
import tcod.event
import tcod.console

import input_handlers


def main():
    screen_width = 80
    screen_height = 60
    panel_height = int(screen_height / 2)

    player_x = int(screen_width / 2)
    player_y = int(screen_height / 2)

    libtcod.console_set_custom_font("img/terminal12x12_gs_ro.png",
                                    libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_CP437)
    libtcod.sys_set_fps(60)
    root = libtcod.console_init_root(screen_width, screen_height, 'PyRL', False, renderer=libtcod.RENDERER_SDL2)
    con = libtcod.console.Console(screen_width, screen_height)
    panel = libtcod.console.Console(screen_width, panel_height)

    # root.print(screen_width // 2 - 7, screen_height // 2 - 12, 'RogueSouls', fg=libtcod.crimson,
    #            bg=libtcod.darkest_han)
    # root.print(screen_width // 2 - 8, screen_height // 2 - 10, 'By Jerezereh')

    while True:
        libtcod.console_put_char(con, player_x, player_y, '@', libtcod.BKGND_NONE)
        libtcod.console_blit(con, 0, 0, screen_width, screen_height, root, 0, 0)
        libtcod.console_flush()

        for event in libtcod.event.get():
            if event.type == "QUIT":
                return True
            if event.type == "KEYDOWN":
                action = input_handlers.handle_keys(event)
            else:
                action = None

            if action is not None:
                move = action.get('move')
                exit = action.get('exit')
                fullscreen = action.get('fullscreen')

                if move:
                    dx, dy = move
                    player_x += dx
                    player_y += dy

                if exit:
                    return True

                if fullscreen:
                    libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())


if __name__ == "__main__":
    main()
