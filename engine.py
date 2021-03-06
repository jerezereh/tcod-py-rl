import tcod as libtcod
import tcod.event
import tcod.console

from components.inventory import Inventory
from death_functions import kill_monster, kill_player
from game_messages import MessageLog, Message
from input_handlers import handle_keys
from components.fighter import Fighter
from entity import Entity, get_blocking_entities_at_location
from fov_functions import initialize_fov, recompute_fov
from game_states import GameStates
from map_objects.game_map import GameMap
from render_functions import clear_all, render_all, RenderOrder


def main():
    screen_width = 80
    screen_height = 50

    bar_width = 20
    panel_height = 7
    panel_y = screen_height - panel_height

    message_x = bar_width + 2
    message_width = screen_width - bar_width - 2
    message_height = panel_height - 1

    map_width = 80
    map_height = 43

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    max_monsters_per_room = 3
    max_items_per_room = 2

    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 10

    colors = {
        'dark_wall': libtcod.Color(0, 0, 100),
        'dark_ground': libtcod.Color(50, 50, 150),
        'light_wall': libtcod.Color(130, 110, 50),
        'light_ground': libtcod.Color(200, 180, 50)
    }

    inventory_component = Inventory(26)
    fighter_component = Fighter(hp=30, defense=2, power=5)
    player = Entity(0, 0, '@', libtcod.white, 'Player', blocks=True, render_order=RenderOrder.ACTOR,
                    fighter=fighter_component, inventory=inventory_component)
    entities = [player]

    libtcod.console_set_custom_font("img/terminal12x12_gs_ro.png",
                                    libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_CP437)
    libtcod.sys_set_fps(60)
    root = libtcod.console_init_root(screen_width, screen_height, 'PyRL', False, renderer=libtcod.RENDERER_SDL2)
    con = libtcod.console.Console(screen_width, screen_height)
    panel = libtcod.console.Console(screen_width, panel_height)

    # root.print(screen_width // 2 - 7, screen_height // 2 - 12, 'RogueSouls', fg=libtcod.crimson,
    #            bg=libtcod.darkest_han)
    # root.print(screen_width // 2 - 8, screen_height // 2 - 10, 'By Jerezereh')

    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities,
                      max_monsters_per_room, max_items_per_room)

    fov_recompute = True
    fov_map = initialize_fov(game_map)
    message_log = MessageLog(message_x, message_width, message_height)
    game_state = GameStates.PLAYER_TURN
    previous_game_state = game_state
    mouse = None

    while True:
        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)
        render_all(con, panel, root, entities, player, game_map, fov_map, fov_recompute, message_log,
                   screen_width, screen_height, bar_width, panel_height, panel_y, mouse, colors, game_state)
        fov_recompute = False
        libtcod.console_flush()
        clear_all(con, entities)

        for event in libtcod.event.get():
            if event.type == "QUIT":
                return True
            elif event.type == "KEYDOWN":
                action = handle_keys(event, game_state)
            elif event.type == "MOUSEMOTION":
                action = None
                mouse = event
            else:
                action = None

            if action is not None:
                move = action.get('move')
                pickup = action.get('pickup')
                show_inventory = action.get('show_inventory')
                inventory_index = action.get('inventory_index')
                drop_inventory = action.get('drop_inventory')
                exit = action.get('exit')
                fullscreen = action.get('fullscreen')

                player_turn_results = []

                if move and game_state == GameStates.PLAYER_TURN:
                    dx, dy = move
                    destination_x = player.x + dx
                    destination_y = player.y + dy
                    if not game_map.is_blocked(destination_x, destination_y):
                        target = get_blocking_entities_at_location(entities, destination_x, destination_y)

                        if target:
                            attack_results = player.fighter.attack(target)
                            player_turn_results.extend(attack_results)
                        else:
                            player.move(dx, dy)
                            fov_recompute = True
                        game_state = GameStates.ENEMY_TURN

                elif pickup and game_state == GameStates.PLAYER_TURN:
                    for entity in entities:
                        if entity.item and entity.x == player.x and entity.y == player.y:
                            pickup_results = player.inventory.add_item(entity)
                            player_turn_results.extend(pickup_results)
                            break
                    else:
                        message_log.add_message(Message('There is nothing here to pick up.', libtcod.yellow))

                elif show_inventory:
                    previous_game_state = game_state
                    game_state = GameStates.SHOW_INVENTORY

                elif drop_inventory:
                    previous_game_state = game_state
                    game_state = GameStates.DROP_INVENTORY

                elif inventory_index is not None and previous_game_state != GameStates.PLAYER_DEAD and \
                        inventory_index < len(player.inventory.items):
                    item = player.inventory.items[inventory_index]

                    if game_state == GameStates.SHOW_INVENTORY:
                        player_turn_results.extend(player.inventory.use(item))
                    elif game_state == GameStates.DROP_INVENTORY:
                        player_turn_results.extend(player.inventory.drop_item(item))

                elif exit:
                    if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
                        game_state = previous_game_state
                    else:
                        return True

                elif fullscreen:
                    libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

                for player_turn_result in player_turn_results:
                    message = player_turn_result.get('message')
                    dead_entity = player_turn_result.get('dead')
                    item_added = player_turn_result.get('item_added')
                    item_consumed = player_turn_result.get('consumed')
                    item_dropped = player_turn_result.get('item_dropped')

                    if message:
                        message_log.add_message(message)

                    if dead_entity:
                        if dead_entity == player:
                            message, game_state = kill_player(dead_entity)
                        else:
                            message = kill_monster(dead_entity)
                        message_log.add_message(message)

                    if item_added:
                        entities.remove(item_added)
                        game_state = GameStates.ENEMY_TURN

                    if item_consumed:
                        game_state = GameStates.ENEMY_TURN

                    if item_dropped:
                        entities.append(item_dropped)
                        game_state = GameStates.ENEMY_TURN

                if game_state == GameStates.ENEMY_TURN:
                    for entity in entities:
                        if entity.ai:
                            enemy_turn_results = entity.ai.take_turn(player, fov_map, game_map, entities)

                            for enemy_turn_result in enemy_turn_results:
                                message = enemy_turn_result.get('message')
                                dead_entity = enemy_turn_result.get('dead')

                                if message:
                                    message_log.add_message(message)

                                if dead_entity:
                                    if dead_entity == player:
                                        message, game_state = kill_player(dead_entity)
                                    else:
                                        message = kill_monster(dead_entity)
                                    message_log.add_message(message)

                                    if game_state == GameStates.PLAYER_DEAD:
                                        break

                        if game_state == GameStates.PLAYER_DEAD:
                            break

                    else:
                        game_state = GameStates.PLAYER_TURN


if __name__ == "__main__":
    main()
