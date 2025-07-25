import logging
from random import randint, choice
from math import sin
from scripts.Managers.GameAssets import *
from scripts.Entities.Particle import Particle
from functools import cache


SMOKE_TEXTURES = [
    # pg.image.load("assets/entities/smoke1.png"),
    pg.image.load("assets/entities/smoke2.png"),
    # pg.image.load("assets/entities/smoke3.png"),
]

cashed_smoke_textures = {}


@cache
def cached_sin(n):
    return sin(n)


class Building:

    def __init__(self, code, pos: Vector, parent, texture, hp, texture_offset: Vector, item_name, instrument_type,
                 class_id=0, punch_sound=None, break_sound=None, ui_id=None, hitbox_size=None, hitbox_offset=None,
                 collider_hitbox_size=None, collider_hitbox_offset=None, texture_size=Vector(1, 1),
                 use_hibox: bool = True, forced_updating: bool = False):

        self.code = code
        self.hp = hp
        self.pos = pos
        self.parent = parent
        self.texture = texture
        self.texture_offset = texture_offset
        self.item = item_name
        self.punch_sound = punch_sound
        self.break_sound = break_sound
        self.instrument_type = instrument_type
        self.ui_id = ui_id
        self.class_id = class_id
        self.hitbox_size = hitbox_size
        self.hitbox_offset = hitbox_offset
        self.touching_hitbox_size = collider_hitbox_size
        self.touching_hitbox_offset = collider_hitbox_offset
        self.use_hitbox = use_hibox
        self.forced_updating = forced_updating
        self.active = False
        self.anim_speed_val = 20
        self.anim_val = 10
        try:
            self.texture_size = from_iterable(self.texture.get_size())
        except AttributeError:
            try: self.texture_size = from_iterable(self.texture[0].get_size())
            except: self.texture_size = texture_size
        self.screen_pos = Vector(0, 0)
        self.rect = pg.Rect((0, 0, hitbox_size.x, hitbox_size.y)) if hitbox_size else pg.Rect((0, 0, self.texture_size.x, self.texture_size.y))
        self.hitbox = pg.Rect((0, 0, collider_hitbox_size.x, collider_hitbox_size.y)) if collider_hitbox_size else pg.Rect((0, 0, self.texture_size.x, self.texture_size.y))
        self.do_draw = False
        self.touching = False
        self.just_pressed = False
        self.tobeddeleted = False
        self.animation = False
        self.animation_counter = 0

    @staticmethod
    def _handle_tank_interraction(tank, input_slot, output_slot, outout_tank: bool = False):

        if input_slot.item_name:

            liquid = ITEM_TO_LIQUID.get(input_slot.item_name, None)
            if liquid and not outout_tank:
                if tank.can_pump_in(liquid, 10) and output_slot.can_fit("bucket"):
                    tank.pump_in(liquid, 10)
                    input_slot.pop(1)
                    output_slot.append("bucket", 1)
            elif input_slot.item_name == "bucket" and output_slot.can_fit(LIQUID_TO_ITEM[tank.current_liquid]):
                if tank.has(None, 10):
                    input_slot.pop(1)
                    output_slot.append(LIQUID_TO_ITEM[tank.current_liquid], 1)
                    tank.pump_out(10)

    def select_texture(self) -> pg.Surface:

        return self.texture

    def drop_items(self):

        self.parent.drop_items(self.pos, self.item, 1)

    def _calculate_active_texture_size(self) -> Vector:

        return Vector(cached_sin(self.parent.animation_counter / self.anim_speed_val) * self.anim_val, cached_sin(self.parent.animation_counter / self.anim_speed_val) * self.anim_val)

    def draw(self):

        if self.do_draw:
            if self.active:
                val = self._calculate_active_texture_size()
                pos = self.screen_pos + (Vector(-0.25, -1)*val) / Vector(0.5, 1)
                texture = pg.transform.scale(self.select_texture(), (self.texture_size + val).as_tuple())
            else:
                texture = self.select_texture()
                pos = self.screen_pos
            screen.blit(texture, pos.as_tuple())
            if self.touching: draw_brackets(screen, self.rect)
            self.draw_secret_data()

    def draw_secret_data(self):

        if self.parent.show_secret_data:
            pg.draw.circle(screen, "#ff00ff", (self.pos+self.parent.offset).as_tuple(), 5)
            pg.draw.rect(screen, "#ff0000", self.hitbox, 3)

    def update(self, preview_mode: bool = False):

        self.screen_pos = self.pos + self.parent.offset + self.texture_offset + (
            pg.math.Vector2(0, 0) if not self.animation else pg.math.Vector2(randint(-2, 2), randint(-2, 2)))
        self.do_draw = all([
            self.screen_pos.x < RESOLUTION.x,
            self.screen_pos.x > -self.texture_size.x,
            self.screen_pos.y < RESOLUTION.y,
            self.screen_pos.y > -self.texture_size.y,
        ])
        if self.do_draw:

            self.rect.x = self.screen_pos.x
            self.rect.y = self.screen_pos.y

            self.hitbox.x = self.screen_pos.x
            self.hitbox.y = self.screen_pos.y

            if self.hitbox_offset:
                self.rect.x += self.hitbox_offset.x
                self.rect.y += self.hitbox_offset.y

            if self.touching_hitbox_offset:
                self.hitbox.x += self.touching_hitbox_offset.x
                self.hitbox.y += self.touching_hitbox_offset.y

            player_item = items.setdefault(self.parent.inventory.n[self.parent.player.inventory_cursor], None)
            if not (self.instrument_type is None):
                try: type_match = player_item.type_ == self.instrument_type
                except: type_match = False
            else:
                type_match = True

            if self.ui_id is not None:
                self.touching = self.rect.collidepoint(get_mouse_pos()) and self.parent.active_ui_id is None
            else:
                self.touching = self.rect.collidepoint(get_mouse_pos()) and self.parent.active_ui_id is None and player_item and type_match

            if self.touching and pg.mouse.get_pressed()[2] and not self.just_pressed and not self.ui_id is None and not preview_mode:
                self.just_pressed = True
                self.parent.UIs[self.ui_id].when_opened()
                self.parent.active_ui_id = self.ui_id
                self.parent.active_object_ui = self
                logging.info(f"{self.ui_id} opened")

        if self.touching and pg.mouse.get_pressed()[0] and player_item and type_match and not preview_mode:

            if player_item.dont_need_clicking:

                if self.parent.animation_counter % 15 == 0 and self.punch_sound:
                    self.punch_sound.stop()
                    self.punch_sound.play()

                self.hp -= player_item.damage
                self.animation = True
                if self.hp <= 0:
                    self.drop_items()
                    if self.break_sound:
                        self.break_sound.stop()
                        self.break_sound.play()
                    self.tobeddeleted = True
                    return

            else:

                if not self.just_pressed:

                    self.just_pressed = True
                    self.hp -= player_item.damage
                    self.animation = True
                    if self.punch_sound:
                        self.punch_sound.stop()
                        self.punch_sound.play()
                    if self.hp <= 0:
                        if self.break_sound:
                            self.break_sound.stop()
                            self.break_sound.play()
                        self.drop_items()
                        self.tobeddeleted = True
                        return

        if self.just_pressed and not (pg.mouse.get_pressed()[0] or pg.mouse.get_pressed()[2]):
            self.just_pressed = False

        if self.animation:
            self.animation_counter += 1

        if self.animation_counter >= 10:
            self.animation_counter = 0
            self.animation = False

    def dumb(self) -> dict:

        return {
            "class": self.__class__.__name__,
            "pos": self.pos.as_tuple()
        }

    def load(self, data: dict):

        self.pos = from_iterable(data["pos"])

    def __repr__(self):

        return f"Building at {self.pos}"

    def summon_smoke(self, pos: Vector, size: tuple, color=None, delta_trans=-0.0000001, initial_trans=50, living_time=100):

        smoke_texture_id = randint(0, len(SMOKE_TEXTURES) - 1)
        if (size, smoke_texture_id, color) in cashed_smoke_textures:
            texture = cashed_smoke_textures[(size, smoke_texture_id, color)].copy()
        else:
            texture = pg.transform.scale(choice(SMOKE_TEXTURES), size)
            if color:
                texture = replace_color(texture, (0, 0, 0, 255), color)
            texture.set_alpha(initial_trans)
            cashed_smoke_textures[(size, smoke_texture_id, color)] = texture.copy()
        delta_size = Vector(0.5, 0.5)
        obj = Particle(self.parent.generate_id(), pos, self.parent, Vector(1, -2), living_time, texture, gravity=False,
                       delta_size_per_update=delta_size, delta_transparency=delta_trans)
        self.parent.particles.append(obj)
