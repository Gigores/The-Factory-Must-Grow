import logging
from time import time_ns

import pygame as pg

from scripts.Entities.ABC.Wall import Wall
from scripts.constants import *
from scripts.Managers.GameAssets import *
from scripts.Entities.ABC.ElectricNode import ElectricNode
from scripts.Entities.Buildings.Wire import Wire
from datetime import *
from random import randint
import math
import subprocess
import psutil

from scripts.Classes.ABC.Scene import Scene
from scripts.Classes.Registry.SceneRegistry import SceneRegistry


def draw_pie_chart(screen, values, colors, center=(200, 200), radius=150):
    total_value = sum(values)
    start_angle = 0

    for i, value in enumerate(values) :
        # Calculate the proportion of each segment in degrees
        end_angle = start_angle + (value / total_value) * 360

        # Convert angles from degrees to radians
        start_radian = math.radians(start_angle)
        end_radian = math.radians(end_angle)

        # Create a list of points for the pie slice
        points = [center]  # Start at the center
        point_count = 30  # Number of points to approximate the arc

        # Generate points along the arc
        for j in range(point_count + 1):
            angle = start_radian + (end_radian - start_radian) * j / point_count
            x = center[0] + math.cos(angle) * radius
            y = center[1] + math.sin(angle) * radius
            points.append((x, y))

        # Draw the pie slice
        pg.draw.polygon(screen, colors[i % len(colors)], points)

        # Move to the next segment
        start_angle = end_angle


class GameScene(Scene, metaclass=SceneRegistry):

    def __init__(self, parent):

        super().__init__(parent)
        self.cursor_obj = None

        self.process = psutil.Process(os.getpid())
        self.os_process_id = os.getpid()
        self.rendering_time = 0
        self.updating_time = 0
        self.input_handling_time = 0
        self.last_wire_connection = None

    def hang_wire(self, entity):
        self.parent.wires.append(Wire(self.parent.faker.unique.random_int(min=0, max=4294967295), (0, 0), self.parent, self.last_wire_connection, entity.code))
        self.last_wire_connection = entity.code

    def handle_key_down_event(self, event, ui_opened):

        settings = self.parent.settings_manager.settings

        if event.key == settings["go_up"] and not ui_opened :
            self.parent.go_up = True

        if event.key == settings["go_left"] and not ui_opened :
            self.parent.go_left = True

        if event.key == settings["go_down"] and not ui_opened :
            self.parent.go_down = True

        if event.key == settings["go_right"] and not ui_opened :
            self.parent.go_right = True

        if event.key == settings["drop_item"] :
            item = self.parent.inventory.n[self.parent.player.inventory_cursor]
            amount = self.parent.inventory.a[self.parent.player.inventory_cursor] if self.parent.shift_pressed else 1
            if item :
                pos = from_iterable(get_mouse_pos()) - self.parent.offset
                self.parent.drop_items(pos, item, amount)
                self.parent.inventory.pop_from_slot(self.parent.player.inventory_cursor, amount)

        if event.key == pg.K_ESCAPE:
            logging.info("Opening escape menu")
            if ui_opened :
                self.parent.active_ui_id = None
                self.parent.active_object_ui = None
            else :
                self.parent.active_ui_id = "ESCMenu"

        if event.key == settings["achievements"] and (self.parent.active_ui_id == "AchivemenMenu" or self.parent.active_ui_id is None) and not (self.parent.active_ui_id == "TerminalWindow"):
            logging.info("Opening achievements menu")
            if self.parent.active_ui_id == "AchivemenMenu" :
                self.parent.active_ui_id = None
                self.parent.active_object_ui = None
            else :
                self.parent.active_ui_id = "AchivemenMenu"

        if event.key == settings["backpack"] and not (self.parent.active_ui_id == "TerminalWindow"):
            logging.info("Opening backpack menu")
            if self.parent.active_ui_id == "BackpackUI":
                self.parent.active_ui_id = None
                self.parent.active_object_ui = None
            else:
                if self.parent.active_ui_id is None:
                    self.parent.active_ui_id = "BackpackUI"
                else:
                    self.parent.active_ui_id = None
                    self.parent.active_object_ui = None

        if event.key == settings["hide_ui"] :
            self.parent.show_ui = not self.parent.show_ui

        if event.key == settings["screenshot"] :
            file_name = f"{datetime.now()}.png".replace(":", "-")
            file_path = os.path.join(APPDATA_FOLDER_PATH, SCREENSHOT_FOLDER, file_name)
            pg.image.save(screen, file_path)
            SCREENSHOT_SOUND.stop()
            SCREENSHOT_SOUND.play()
            logging.info(f"Screenshot saved as {file_name}")

        if event.key == settings["map"] and (self.parent.active_ui_id == "MapUI" or self.parent.active_ui_id is None):
            logging.info("Opening map menu")
            if self.parent.active_ui_id == "MapUI" :
                self.parent.active_ui_id = None
                self.parent.active_object_ui = None
            else :
                self.parent.active_ui_id = "MapUI"
                self.parent.UIs["MapUI"].update_map_texture()

        if event.key == pg.K_F3:
            self.parent.show_secret_data = not self.parent.show_secret_data

        if event.key == settings["terminal"] and (self.parent.active_ui_id == "TerminalWindow" or self.parent.active_ui_id is None) and settings["enable_terminal"] :
            logging.info("Opening terminal")
            if self.parent.active_ui_id == "TerminalWindow" :
                self.parent.active_ui_id = None
                self.parent.active_object_ui = None
            else :
                self.parent.active_ui_id = "TerminalWindow"

        if event.key == pg.K_LSHIFT :
            self.parent.shift_pressed = True

        if event.key == pg.K_LCTRL :
            self.parent.ctrl_pressed = True

        if event.key == pg.K_LALT :
            self.parent.alt_pressed = True

    def handle_key_up_event(self, event):

        settings = self.parent.settings_manager.settings

        if event.key == settings["go_up"] :
            self.parent.go_up = False

        if event.key == settings["go_left"] :
            self.parent.go_left = False

        if event.key == settings["go_down"] :
            self.parent.go_down = False

        if event.key == settings["go_right"] :
            self.parent.go_right = False

        if event.key == pg.K_LSHIFT :
            self.parent.shift_pressed = False

        if event.key == pg.K_LCTRL :
            self.parent.ctrl_pressed = False

        if event.key == pg.K_LALT :
            self.parent.alt_pressed = False

    def update_cursor_item(self):

        if self.parent.player.inventory_cursor < 0:
            self.parent.player.inventory_cursor = INVENTORY_SIZE - 1
        elif self.parent.player.inventory_cursor > INVENTORY_SIZE - 1:
            self.parent.player.inventory_cursor = 0
        self.parent.inventory.reset_animation()
        player_cursor_item = items.setdefault(self.parent.inventory.n[self.parent.player.inventory_cursor], None)
        if player_cursor_item:
            if isinstance(player_cursor_item, BuildingItem) and player_cursor_item.entity == "Wire":
                self.last_wire_connection = None
            elif isinstance(player_cursor_item, BuildingItem):
                unique_id = self.parent.faker.unique.random_int(min=0, max=4294967295)
                pos = Vector(get_mouse_pos()[0], get_mouse_pos()[1]) - self.parent.offset
                self.cursor_obj = self.parent.str_to_entity[player_cursor_item.entity](unique_id, pos, self.parent)

    def handle_mouse_button_event(self, event, ui_opened, player_cursor_item, can_place):

        if event.button == 5 and not ui_opened :
            self.parent.inventory.last_active = self.parent.player.inventory_cursor
            self.parent.player.inventory_cursor += 1
            self.update_cursor_item()

        if event.button == 4 and not ui_opened :
            self.parent.inventory.last_active = self.parent.player.inventory_cursor
            self.parent.player.inventory_cursor -= 1
            self.update_cursor_item()

        if event.button == 3 and self.last_wire_connection :
            self.last_wire_connection = None

        if event.button == 1 and self.parent.active_ui_id is None :
            if isinstance(player_cursor_item, BuildingItem) :
                if player_cursor_item.entity == "Wire" :
                    for entity in sorted(self.parent.entities_to_draw,
                                         key=lambda e : e.pos.y and isinstance(e, ElectricNode)) :
                        if hasattr(entity, "rect") and entity.rect.collidepoint(get_mouse_pos()) and isinstance(entity,
                                                                                                                ElectricNode) :
                            # if self.parent.entity_manager.get_building_connections_amount(entity.code) < entity.max_connections:
                            if not self.last_wire_connection :
                                self.last_wire_connection = entity.code
                            else :
                                if self.last_wire_connection != entity.code and self.last_wire_connection is not None :
                                    wire = self.parent.entity_manager.get_wire_by_connections(self.last_wire_connection,
                                                                                              entity.code)
                                    print(wire)
                                    if wire is None :
                                        last_wire_connection_entity = self.parent.entity_manager.get_building_by_code(
                                            self.last_wire_connection)
                                        # print(self.parent.entity_manager.get_building_connections_amount(entity.code), entity.max_connections, self.parent.entity_manager.get_building_connections_amount(last_wire_connection_entity), last_wire_connection_entity.max_connections)
                                        # print(entity.code, self.last_wire_connection)
                                        if self.parent.entity_manager.get_building_connections_amount(
                                                entity.code) < entity.max_connections and self.parent.entity_manager.get_building_connections_amount(
                                                self.last_wire_connection) < last_wire_connection_entity.max_connections and distance(
                                                self.parent.entity_manager.get_building_by_code(
                                                        self.last_wire_connection).pos, entity.pos) < TILE_SIZE.x * 10 :
                                            # if self.parent.entity_manager.get_building_connections_amount(self.last_wire_connection) > 0 and self.parent.entity_manager.get_building_connections_amount(entity.code) > 0 and distance(self.parent.entity_manager.get_building_by_code(self.last_wire_connection).pos, entity.pos) < TILE_SIZE.x * 10:
                                            self.hang_wire(entity)
                                    else :
                                        self.parent.entity_manager.get_wire_by_connections(self.last_wire_connection,
                                                                                           entity.code).tobedeleted = True
                                        self.last_wire_connection = None
                else :
                    if can_place :
                        self.parent.inventory.pop_from_slot(self.parent.player.inventory_cursor)
                        unique_id = self.parent.faker.unique.random_int(min=0, max=4294967295)
                        if self.parent.shift_pressed :
                            pos = (Vector(
                                get_mouse_pos()) - self.parent.offset) // TILE_SIZE * TILE_SIZE + TILE_SIZE / 2
                        else :
                            pos = Vector(get_mouse_pos()) - self.parent.offset
                        obj = self.parent.str_to_entity[player_cursor_item.entity](unique_id, pos, self.parent)
                        self.parent.buildings.append(obj)
                        if player_cursor_item.entity not in self.parent.all_placed_buildings :
                            self.parent.all_placed_buildings.append(player_cursor_item.entity)
                            self.parent.update_achievements()
                            logging.info(f"'{player_cursor_item.entity}' placed at {pos}")
                        PLACING_SOUND.play()
                        self.parent.entity_manager.update_entities_by_chunks()
                        self.parent.entity_manager.update_active_chunks()
                        self.cursor_obj = self.parent.str_to_entity[player_cursor_item.entity](unique_id, pos,
                                                                                               self.parent)
            elif isinstance(player_cursor_item, PlaceableTile) :
                tile_x = int((get_mouse_pos()[0] - self.parent.offset.x) // TILE_SIZE.x)
                tile_y = int((get_mouse_pos()[1] - self.parent.offset.y) // TILE_SIZE.y)
                if self.parent.world.data[tile_x][tile_y] not in player_cursor_item.unchangeable_tiles and (
                        self.parent.world.data[tile_x][tile_y] in player_cursor_item.avilable_tiles or not len(
                        player_cursor_item.avilable_tiles)) :
                    self.parent.world.data[tile_x][tile_y] = player_cursor_item.tile_id
                    if player_cursor_item.item_deleting :
                        self.parent.inventory.pop_from_slot(self.parent.player.inventory_cursor, 1)
                    self.parent.world.update_chunk(tile_x // CHUNK_SIZE.x, tile_y // CHUNK_SIZE.y)
                    logging.info(f"'{player_cursor_item.tile_id}' tile placed at ({tile_x}, {tile_y})")
            elif isinstance(player_cursor_item, Tool) and player_cursor_item.type_ == "shovel" :
                tile_x = int((get_mouse_pos()[0] - self.parent.offset.x) // TILE_SIZE.x)
                tile_y = int((get_mouse_pos()[1] - self.parent.offset.y) // TILE_SIZE.y)
                tile_pos = Vector(tile_x, tile_y)
                tile = self.parent.world.get(tile_pos)
                item = TILE_TO_ITEM.setdefault(str(tile))
                force = Vector(-3 * (1 if randint(0, 1) else -1), 5)
                if item :
                    item_pos = tile_pos * TILE_SIZE + Vector(randint(0, TILE_SIZE.x), randint(0, TILE_SIZE.y))
                    self.parent.drop_items(item_pos, item, 1, force)
                    self.parent.entity_manager.update_entities_by_chunks()
            elif isinstance(player_cursor_item, Tool) and player_cursor_item.type_ == "hoe" :
                tile_x = int((get_mouse_pos()[0] - self.parent.offset.x) // TILE_SIZE.x)
                tile_y = int((get_mouse_pos()[1] - self.parent.offset.y) // TILE_SIZE.y)
                tile_pos = Vector(tile_x, tile_y)
                tile = self.parent.world.get(tile_pos)
                if tile in [0, 1] :
                    self.parent.world.data[tile_x][tile_y] = 9
                    self.parent.world.update_chunk(tile_x // CHUNK_SIZE.x, tile_y // CHUNK_SIZE.y)
                    logging.info(f"'9' tile placed at ({tile_x}, {tile_y})")
            elif isinstance(player_cursor_item, Food) :
                current_value = getattr(self.parent.player, player_cursor_item.affects)
                max_value = {"hunger" : MAX_PLAYER_HUNGER, "health" : MAX_PLAYER_HEALTH}[
                    player_cursor_item.affects]
                if ((
                            player_cursor_item.saturation_level > 0 and current_value < max_value) or player_cursor_item.saturation_level < 0) or not \
                self.parent.settings_manager.settings["survival_mode"] :
                    new_value = current_value + player_cursor_item.saturation_level
                    setattr(self.parent.player, player_cursor_item.affects, new_value)
                    self.parent.inventory.pop_from_slot(self.parent.player.inventory_cursor)
                    EATING_SOUND.stop()
                    EATING_SOUND.play()
                    if player_cursor_item.saturation_level < 0 :
                        self.parent.player.check_is_dead()
            elif self.parent.inventory.n[self.parent.player.inventory_cursor] == "bucket" :
                tile_x = int((get_mouse_pos()[0] - self.parent.offset.x) // TILE_SIZE.x)
                tile_y = int((get_mouse_pos()[1] - self.parent.offset.y) // TILE_SIZE.y)
                print(str(self.parent.world.get(Vector(tile_x, tile_y))), TILE_TO_BUCKET)
                bucket_item = TILE_TO_BUCKET.get(str(self.parent.world.get(Vector(tile_x, tile_y))), None)
                if bucket_item :
                    self.parent.inventory.pop_from_slot(self.parent.player.inventory_cursor, 1)
                    self.parent.inventory.append(bucket_item)
            elif self.parent.inventory.n[self.parent.player.inventory_cursor] in TILE_TO_BUCKET.values() :
                tile_x = int((get_mouse_pos()[0] - self.parent.offset.x) // TILE_SIZE.x)
                tile_y = int((get_mouse_pos()[1] - self.parent.offset.y) // TILE_SIZE.y)
                if str(self.parent.world.get(Vector(tile_x, tile_y))) in TILE_TO_BUCKET and "bucket" in items :
                    self.parent.inventory.pop_from_slot(self.parent.player.inventory_cursor, 1)
                    self.parent.inventory.append("bucket")
            player_cursor_item = items.setdefault(self.parent.inventory.n[self.parent.player.inventory_cursor], None)

    def handle_events(self, events: list[pg.event.Event]):

        t0 = time_ns()

        def update_cursor_obj():

            player_cursor_item = items.setdefault(self.parent.inventory.n[self.parent.player.inventory_cursor], None)

        cursor_tile_x = int((get_mouse_pos()[0] - self.parent.offset.x) // TILE_SIZE.x)
        cursor_tile_y = int((get_mouse_pos()[1] - self.parent.offset.y) // TILE_SIZE.y)

        ui_opened = self.parent.active_ui_id is not None
        player_cursor_item = items.setdefault(self.parent.inventory.n[self.parent.player.inventory_cursor], None)
        can_place = True

        should_draw_building_texture = isinstance(player_cursor_item, BuildingItem) and player_cursor_item.entity != "Wire" and self.cursor_obj
        if should_draw_building_texture :
            # unique_id = self.parent.faker.unique.random_int(0, 4294967295)
            pos = Vector(get_mouse_pos()) - self.parent.offset
            self.cursor_obj.pos = pos
            self.cursor_obj.update(preview_mode=True)

            can_place = True
            if hasattr(self.cursor_obj, 'hitbox') :
                if any(hasattr(entity, 'hitbox') and entity.hitbox.colliderect(self.cursor_obj.hitbox) for entity in sorted(self.parent.entities_to_draw, key=lambda e : distance(e.pos, self.cursor_obj.pos))) :
                    can_place = False

            cursor_tile = self.parent.world.data[cursor_tile_x][cursor_tile_y]
            if not tiles[cursor_tile].walkable or (hasattr(self.cursor_obj, 'hitbox') and self.cursor_obj.hitbox.collidepoint((self.parent.player.pos + self.parent.offset).as_tuple())) :
                can_place = False

            if player_cursor_item.available_tiles and cursor_tile not in player_cursor_item.available_tiles :
                can_place = False

        for event in events:

            if event.type == pg.QUIT:
                self.parent.running = False

            elif event.type == pg.KEYDOWN:

                self.handle_key_down_event(event, ui_opened)

            elif event.type == pg.KEYUP :

                self.handle_key_up_event(event)

            elif event.type == pg.MOUSEBUTTONDOWN :

                self.handle_mouse_button_event(event, ui_opened, player_cursor_item,
                                               can_place)

        if self.parent.active_ui_id is not None:

            self.parent.UIs[self.parent.active_ui_id].events(events)

        self.input_handling_time = (time_ns() - t0) * 1e-6

    def update(self):

        t0 = time_ns()

        # self.parent.offset = Vector(-1, -1) * self.parent.player.pos + RESOLUTION / Vector(2, 2) - TILE_SIZE * Vector(1.5, 1.5) / Vector(2, 2)
        follow_speed = Vector(0.1, 0.1)
        target_offset = (Vector(-1, -1) * self.parent.player.pos + RESOLUTION / Vector(2, 2) -
                         TILE_SIZE * Vector(1.5,1.5) / Vector(2, 2))
        self.parent.offset += (target_offset - self.parent.offset) * follow_speed

        ui_opened = self.parent.active_ui_id != None

        self.parent.player.move(Vector(int(self.parent.go_left) * -1 + int(self.parent.go_right),
                                       int(self.parent.go_up) * -1 + int(self.parent.go_down)))

        # if new_player_chunk_y != player_chunk_y or new_player_chunk_x != player_chunk_x:
        #     self.parent.entity_manager.update_active_chunks()

        if self.parent.animation_counter % 30 == 0:

            if any([self.parent.go_up, self.parent.go_left, self.parent.go_down, self.parent.go_right]) :
                sound_id = int(self.parent.animation_counter % (30 * len(FOOTSTEP_SOUNDS)) / 30)
                # FOOTSTEP_SOUNDS[sound_id].play()

        if self.parent.animation_counter % 10 == 0:
            self.parent.entity_manager.update_active_chunks()
        self.parent.entity_manager.update_entities()
        if self.parent.animation_counter % (FPS * 5 - 1) == 0:
            self.parent.entity_manager.calculate_subnetworks()
        if self.parent.animation_counter % (FPS - 1) == 0:
            self.parent.entity_manager.calculate_subnetworks_balances_and_distribute()
        self.parent.inventory.update()
        self.parent.achievements_visuals_manager.update()

        #if ui_opened:
        #    self.parent.UIs[self.parent.active_ui_id].update(self.parent.active_object_ui)

        if self.cursor_obj:
            self.cursor_obj.pos = Vector(get_mouse_pos()[0], get_mouse_pos()[1]) - self.parent.offset

        if self.parent.go_up and ui_opened:
            self.parent.go_up = False
        if self.parent.go_down and ui_opened:
            self.parent.go_down = False
        if self.parent.go_left and ui_opened:
            self.parent.go_left = False
        if self.parent.go_right and ui_opened:
            self.parent.go_right = False

        self.updating_time = (time_ns() - t0) * 1e-6

    def draw(self):

        t0 = time_ns()

        mouse_pos = Vector(get_mouse_pos())
        cursor_tile = ((mouse_pos - self.parent.offset) // TILE_SIZE).to_int()

        player_cursor_item = items.setdefault(self.parent.inventory.n[self.parent.player.inventory_cursor], None)
        should_draw_building_texture = isinstance(player_cursor_item, BuildingItem) and player_cursor_item.entity != "Wire"
        should_draw_tile_texture = isinstance(player_cursor_item, PlaceableTile) and player_cursor_item.display_tile
        ui_opened = self.parent.active_ui_id is not None

        screen.fill("#000000")

        self.parent.world.draw()

        entities = self.parent.entities_to_draw + self.parent.wires
        for ent in entities:
            ent.draw()

        # pprint.pprint(self.entities_to_draw)

        if should_draw_building_texture and self.cursor_obj:
            if self.parent.shift_pressed or isinstance(self.cursor_obj, Wall):
                pos = (mouse_pos - self.parent.offset) // TILE_SIZE * TILE_SIZE + TILE_SIZE / 2
            else :
                pos = mouse_pos - self.parent.offset
            self.cursor_obj.pos = pos
            self.cursor_obj.update(True)
            texture_pos = self.cursor_obj.screen_pos
            texture = self.cursor_obj.texture.copy() if isinstance(self.cursor_obj.texture, pg.Surface) else self.cursor_obj.texture[0].copy()
            texture.set_alpha(100)
            screen.blit(texture, texture_pos.as_tuple())
            # pg.draw.rect(screen, "#ff0000", rect_to_draw, 20)
        if should_draw_tile_texture :
            texture = tiles[player_cursor_item.tile_id].texture.copy()
            texture.set_alpha(100)
            screen_pos = cursor_tile * TILE_SIZE + self.parent.offset
            screen.blit(texture, screen_pos.as_tuple())
            rect_texture = pg.Surface(TILE_SIZE.as_tuple())
            pg.draw.rect(rect_texture, "#ffffff", (0, 0, TILE_SIZE.x, TILE_SIZE.y), 4)
            rect_texture.set_alpha(150)
            rect_texture.set_colorkey("#000000")
            screen.blit(rect_texture, screen_pos.as_tuple())
        if self.last_wire_connection is not None:
            entity = self.parent.entity_manager.get_building_by_code(self.last_wire_connection)
            if entity:
                draw_wire(entity.pos + entity.texture_offset - entity.wire_connection_offset + self.parent.offset, mouse_pos)
                # pg.draw.line(screen, "#000000", (entity.pos + entity.texture_offset - entity.wire_connection_offset + self.parent.offset).as_tuple(), get_mouse_pos(), 3)

        if self.parent.show_ui :
            self.parent.inventory.draw()
            if player_cursor_item :
                texture1 = BIG_FONT.render(player_cursor_item.name, True, "#000000")
                texture2 = BIG_FONT.render(player_cursor_item.name, True, "#ffffff")
                item_name_x = (RESOLUTION.x / 2 + 2.5) - texture1.get_width() / 2
                screen.blit(texture1, (item_name_x + 5, INVENTORY_POS.y - BIG_FONT.get_height() * 1.5 + 5))
                screen.blit(texture2, (item_name_x, INVENTORY_POS.y - BIG_FONT.get_height() * 1.5))

            def draw_bar(pos: Vector, size: Vector, color: str, value: int, max_value: int, name: str,
                         revers: bool = False, font: pg.font.Font = FONT) :

                surface = pg.Surface(size.as_tuple())
                surface.set_alpha(128)
                screen.blit(surface, pos.as_tuple())
                if value > max_value :
                    display_value = max_value
                else :
                    display_value = value
                width = (size.x - BAR_BORDER_WIDTH * 2) / max_value * display_value
                if revers :
                    rect = pg.Rect(pos.x + BAR_BORDER_WIDTH + (size.x - BAR_BORDER_WIDTH * 2 - width),
                                   pos.y + BAR_BORDER_WIDTH, width, size.y - BAR_BORDER_WIDTH * 2)
                else :
                    rect = pg.Rect(pos.x + BAR_BORDER_WIDTH, pos.y + BAR_BORDER_WIDTH, width,
                                   size.y - BAR_BORDER_WIDTH * 2)
                pg.draw.rect(screen, color, rect)
                text_surf = font.render(name, True, "#ffffff")
                text_pos = Vector((pos.x + size.x - text_surf.get_width() - BAR_BORDER_WIDTH * 2) if revers else (
                            pos.x + BAR_BORDER_WIDTH * 2),
                                  pos.y + size.y / 2 + BAR_BORDER_WIDTH - text_surf.get_height() / 2)
                screen.blit(text_surf, text_pos.as_tuple())

            if self.parent.settings_manager.settings["survival_mode"]:

                draw_bar(HEALTH_POS, HEALTH_SIZE, "#ff3333", self.parent.player.health, MAX_PLAYER_HEALTH, "health")
                draw_bar(HUNGER_POS, HUNGER_SIZE, "#33bb33", self.parent.player.hunger, MAX_PLAYER_HUNGER, "hunger", True)

        # pg.draw.circle(screen, "#ff0000", (RESOLUTION/Vector(2, 2)).as_tuple(), 5)

        if ui_opened:

            screen.blit(self.parent.DARKNESS, (0, 0))
            self.parent.UIs[self.parent.active_ui_id].draw(screen)
            self.parent.UIs[self.parent.active_ui_id].update(self.parent.active_object_ui)

        self.parent.achievements_visuals_manager.draw()

        self.rendering_time = (time_ns() - t0) * 1e-6

        if self.parent.show_secret_data :
            screen.blit(FONT.render(f"FPS - {self.parent.clock.get_fps()}", True, "#ffffff", "#000000"), (0, 0))
            try: potential_fps = 1000 / (self.input_handling_time + self.updating_time + self.rendering_time)
            except ZeroDivisionError: potential_fps = 1000 / (self.input_handling_time + self.updating_time + self.rendering_time + 1)
            screen.blit(FONT.render(f"potential FPS - {potential_fps}", True, "#ffffff", "#000000"), (0, FONT.get_height()))
            screen.blit(FONT.render(f"player pos - {self.parent.player.pos}", True, "#ffffff", "#000000"),
                        (0, FONT.get_height() * 2))
            # screen.blit(FONT.render(f"current biome - {self.biome_map[self.player.tile_pos.x][self.player.tile_pos.x]}", True, "#ffffff", "#000000"), (0, FONT.get_height() * 2))
            screen.blit(FONT.render("tile data:", True, "#ffffff", "#000000"), (0, FONT.get_height() * 4))
            screen.blit(FONT.render(f"    pos: ({cursor_tile.x}, {cursor_tile.y})", True, "#ffffff", "#000000"),
                        (0, FONT.get_height() * 5))
            tile_data = tiles[self.parent.world.data[cursor_tile.x][cursor_tile.y]].get_data()
            screen.blit(FONT.render(f"    biome: {biome_to_name[self.parent.biome_map[cursor_tile.x][cursor_tile.y]]}", True,
                                    "#ffffff", "#000000"), (0, FONT.get_height() * 6))
            for i, (k, v) in enumerate(tile_data.items()) :
                screen.blit(FONT.render(f"    {k}: {v}", True, "#ffffff", "#000000"), (0, FONT.get_height() * (7 + i)))

            pg.draw.circle(screen, "#ff0000", get_mouse_pos(), 5)

            draw_pie_chart(screen, (self.input_handling_time, self.updating_time, self.rendering_time), ("#ff0000", "#00ff00", "#0000ff"), (RESOLUTION.x - 220, 220), 200)

            pg.draw.circle(screen, "#ff0000", (RESOLUTION.x - 430, 450), 20)
            screen.blit(FONT.render(f"input handling: {self.input_handling_time}ms", True, "#ffffff", "#000000"), (RESOLUTION.x - 405, 435))
            pg.draw.circle(screen, "#00ff00", (RESOLUTION.x - 430, 490), 20)
            screen.blit(FONT.render(f"updating: {self.updating_time}ms", True, "#ffffff", "#000000"), (RESOLUTION.x - 405, 475))
            pg.draw.circle(screen, "#0000ff", (RESOLUTION.x - 430, 530), 20)
            screen.blit(FONT.render(f"rendering: {self.rendering_time}ms", True, "#ffffff", "#000000"), (RESOLUTION.x - 405, 515))
            screen.blit(FONT.render(f"total: {self.input_handling_time + self.updating_time + self.rendering_time}ms", True, "#ffffff", "#000000"), (RESOLUTION.x - 405, 555))

            memory_info = self.process.memory_info()
            memory_usage = memory_info.rss
            total_memory = psutil.virtual_memory().total
            memory_percentage = (memory_usage / total_memory) * 100
            total_memory_gb = total_memory / (1024 ** 3)
            memory_usage_gb = memory_usage / (1024 ** 3)
            draw_pie_chart(screen, (memory_usage, total_memory - memory_usage), ("#00ff00", "#000000"), (RESOLUTION.x - 120, 700), 100)
            screen.blit(FONT.render(f"memory usage", True, "#55ff55", "#000000"), (RESOLUTION.x - 240, 810))
            screen.blit(FONT.render(f"{memory_percentage:.2f}%", True, "#ffffff", "#000000"), (RESOLUTION.x - 240, 810 + FONT.get_height()))
            screen.blit(FONT.render(f"{memory_usage_gb:.1f}gb/{total_memory_gb:.1f}gb", True, "#ffffff", "#000000"), (RESOLUTION.x - 240, 810 + FONT.get_height() * 2))

            """
            result = subprocess.run(
                ["wmic", "path", "Win32_PerfFormattedData_PerfProc_Process", "where", f"IDProcess={self.os_process_id}", "get",
                 "PercentProcessorTime"],
                capture_output=True,
                text=True
            )
            lines = result.stdout.strip().splitlines()
            if len(lines) > 1:
                cpu_usage = float(lines[2].strip())
                draw_pie_chart(screen, (int(cpu_usage), 100 - int(cpu_usage)), ("#ff0000", "#000000"), (RESOLUTION.x - 320, 700), 100)
                screen.blit(FONT.render(f"cpu usage", True, "#ff5555", "#000000"), (RESOLUTION.x - 440, 810))
                screen.blit(FONT.render(f"{cpu_usage:.2f}%", True, "#ffffff", "#000000"), (RESOLUTION.x - 440, 810 + FONT.get_height()))
            """

    def take_thumbnail(self) -> pg.Surface:

        screen.fill("#000000")

        self.parent.world.draw()
        for ent in self.parent.entities_to_draw :
            ent.draw()

        return screen.copy()
