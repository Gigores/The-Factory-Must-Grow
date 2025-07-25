import logging

from scripts.constants import *
from PgHelp import *
from scripts.Managers.IngameManagers.Inventory import Slot
from copy import copy
from scripts.Entities.ABC.Building import Building
from math import sin
from scripts.Managers.GameAssets import furnace_recipies
from scripts.Classes.Registry.EntityRegistry import EntityRegistry
from scripts.Managers.GameAssets import FUEL_WEIGHT


TEXTURE_SIZE = Vector(TILE_SIZE.x, TILE_SIZE.y)
TEXTURES = [
    load_texture("assets/entities/furnace/furnace_empty.png", TEXTURE_SIZE),
    load_texture("assets/entities/furnace/furnace_working.png", TEXTURE_SIZE),
]
TEXTURE_OFFSET = Vector(-(TEXTURE_SIZE.x / 2), -(TEXTURE_SIZE.y / 6 * 5))
SOUND1 = pg.mixer.Sound("sound/pickaxe_1.mp3")
SOUND1.set_volume(0.5)
SOUND2 = pg.mixer.Sound("sound/ore_done.mp3")
SOUND2.set_volume(0.5)
HITBOX_SIZE = TEXTURE_SIZE * Vector(0.9, 0.6)
HITBOX_OFFSET = TEXTURE_SIZE * Vector(0.05, 0.4)


class Furnace(Building, metaclass=EntityRegistry):

    def __init__(self, code, pos, parent):

        super().__init__(code, pos, parent, TEXTURES, 200, TEXTURE_OFFSET,
                         "furnace", "pickaxe", 1, SOUND1, SOUND2,
                         "FurnaceUI", collider_hitbox_size=HITBOX_SIZE, collider_hitbox_offset=HITBOX_OFFSET,
                         forced_updating=True)

        self.fuel_slot = Slot()
        self.ingredient_slot = Slot()
        self.result_slot = Slot()
        self.fuel_left = 0
        self.fuel_start_amount = 100
        self.progress_start = 10
        self.progress = 0
        self.currently_cooking = (None, 0)

    def drop_items(self):

        self.parent.drop_items(self.pos, self.item, 1)
        self.parent.drop_items(self.pos, self.fuel_slot.item_name, self.fuel_slot.item_amount)
        self.parent.drop_items(self.pos, self.ingredient_slot.item_name, self.ingredient_slot.item_amount)
        self.parent.drop_items(self.pos, self.result_slot.item_name, self.result_slot.item_amount)

    def select_texture(self) -> pg.Surface:

        return self.texture[1] if self.fuel_left > 0 else self.texture[0]

    def draw(self):

        if self.do_draw:
            texture = self.select_texture()
            size = (self.texture_size + Vector(-(sin(self.parent.animation_counter / 12) * 8), sin(self.parent.animation_counter / 12) * 8)).as_tuple()
            pos = self.screen_pos
            if self.progress > 0 and self.fuel_left > 0:
                texture = pg.transform.scale(texture, size)
                pos += Vector((self.texture_size.x - size[0]) / 2, self.texture_size.y - size[1])
            self.parent.screen.blit(texture, pos.as_tuple())
            if self.touching: draw_brackets(self.parent.screen, self.rect)
            self.draw_secret_data()

    def update(self, preview_mode: bool = False):

        super().update(preview_mode)

        can_cook = self.ingredient_slot.item_amount > 0 and self.progress == 0 and self.result_slot.can_fit(furnace_recipies.find(self.ingredient_slot.item_name).result[0], furnace_recipies.find(self.ingredient_slot.item_name).result[1])
        can_consume_fuel = self.fuel_slot.item_amount > 0 and self.fuel_left == 0 and self.fuel_slot.item_name in FUEL_WEIGHT.keys()

        if can_cook and (can_consume_fuel or self.fuel_left > 0):
            if can_consume_fuel:
                self.fuel_start_amount = FUEL_WEIGHT[self.fuel_slot.item_name]
                self.fuel_left = FUEL_WEIGHT[self.fuel_slot.item_name]
                self.fuel_slot.pop(1)
            self.progress = furnace_recipies.find(self.ingredient_slot.item_name).weight
            self.progress_start = furnace_recipies.find(self.ingredient_slot.item_name).weight
            self.currently_cooking = furnace_recipies.find(self.ingredient_slot.item_name).result
            self.ingredient_slot.pop(1)

        if self.parent.animation_counter % 3 == 0:
            if self.progress > 0 and self.fuel_left > 0:
                self.progress -= 1
                if self.progress == 0:
                    self.result_slot.append(self.currently_cooking[0], self.currently_cooking[1])
            if self.fuel_left > 0: self.fuel_left -= 1

    def _get_future_recipe(self):

        if self.ingredient_slot.item_amount > 0:
            return furnace_recipies.find(self.ingredient_slot)
        else:
            return None

    def dumb(self) -> dict:

        return {
            "class": self.__class__.__name__,
            "pos": self.pos.as_tuple(),
            "fuel_slot": self.fuel_slot.dumb(),
            "result_slot": self.result_slot.dumb(),
            "ingredient_slot": self.ingredient_slot.dumb(),
            "fuel_left": self.fuel_left,
            "fuel_start": self.fuel_start_amount,
            "progress": self.progress,
            "progress_start": self.progress_start,
            "currently_cooking": self.currently_cooking,
        }

    def load(self, data: dict):

        self.pos = from_iterable(data["pos"])
        self.fuel_slot.load(data["fuel_slot"])
        self.result_slot.load(data["result_slot"])
        self.ingredient_slot.load(data["ingredient_slot"])
        self.fuel_left = copy(data["fuel_left"])
        self.fuel_start_amount = copy(data["fuel_start"])
        self.progress = copy(data["progress"])
        self.progress_start = copy(data["progress_start"])
        self.currently_cooking = copy(data["currently_cooking"])
