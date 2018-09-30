import pygame
from business_logic import validated_by, validator

from src.database.db_tool import DbTool
from src.tools.globals.constants import pixels_changer
from src.events.display.display_tool import DisplayTool
from src.events.logic.errors import Errors


move_choices = {
    (0, -1): pygame.K_UP,
    (0, 1): pygame.K_DOWN,
    (-1, 0): pygame.K_LEFT,
    (1, 0): pygame.K_RIGHT
}


def change_player_coordinates(coordinates_change: tuple):
    player = DbTool().get_player
    x, y = coordinates_change
    player.x += x
    player.y += y
    DisplayTool().refresh()


@validator
def can_move_by_key(key):
    if True:  # TODO check if field is accessible
        return True
    else:
        return None


@validated_by(can_move_by_key)
def move_by_keys(key: pygame.key):
    coordinates_change = 0, 0,
    for co, bounded_key in move_choices.items():
        if bounded_key == key:
            coordinates_change = co
    change_player_coordinates(coordinates_change)


@validator
def can_move_by_mouse(position: tuple):
    if True:  # TODO and when field is accessible
        return True
    else:
        return False


@validated_by(can_move_by_mouse)
def move_by_mouse(position):
    x, y = (coordinate // pixels_changer for coordinate in position)
    x_to_change = [(1, 0) if x - 7 > 0 else (-1, 0) for _ in range(abs(x - 7))]
    y_to_change = [(0, 1) if y - 7 > 0 else (0, -1) for _ in range(abs(y - 7))]
    for coordinates_change in (*x_to_change, *y_to_change):
        change_player_coordinates(coordinates_change)


@validator
def can_collect_item(position: tuple):
    if not is_item_in_player_range(position):
        raise Errors.CANT_INTERACT_WITH_ITEM_TOO_FAR


@validated_by(can_collect_item)
def collect_item(position: tuple):
    player = DbTool().get_player
    item = DbTool().get_element_in_coordinates(('src.objects.items', 'BoundedItem'),
                                                player.x - 7 + position[0] // 64,
                                                player.y - 7 + position[1] // 64)
    columns_to_update = {
        'x': None,
        'y': None,
        'container_id': player.equipment.id_bounded_item,
        'container_slot_id': player.free_eq_slots[0]
    }
    DbTool().update_row(('src.objects.items', 'BoundedItem', 'id_bounded_item'), item.id_bounded_item,
                        columns_to_update)
    DisplayTool().refresh()



# def move_item(from_coordinates, to_coordinates):
#     initial_field = DbTool().get_one_row_where_two_conditions(
#         ('src.objects.fields', 'Field', ('x', 'y')), from_coordinates)
#     target_field = DbTool().get_one_row_where_two_conditions(
#         ('src.objects.fields', 'Field', ('x', 'y')), to_coordinates)
#     columns_to_update = {'field_id': target_field.id_field}
#     DbTool().update_row(('src.objects.items', 'BoundedItem', 'field_id'), initial_field.id_field,
#                         columns_to_update)
# def cancel_move_item():
#     pass
#

@validator
def can_start_drag_item(mouse_input, position: tuple):
    if not is_item_in_player_range(position):
        raise Errors.CANT_INTERACT_WITH_ITEM_TOO_FAR


@validated_by(can_start_drag_item)
def start_drag_item(mouse_input, position: tuple):
    DisplayTool().set_dragged_item(position)


@validator
def can_move_dragged_item(position: tuple):
    return True  # TODO add constraints


@validated_by(can_move_dragged_item)
def move_dragged_item(position):
    DisplayTool().move_dragged_item(position)


def is_item_in_player_range(position):
    player = DbTool().get_player
    return True if (player.x - 7 + position[0] // 64, player.y - 7 + position[1] //64) \
                   in (coordinates for coordinates in DbTool().get_player.get_fields_around_and_self())\
         else False