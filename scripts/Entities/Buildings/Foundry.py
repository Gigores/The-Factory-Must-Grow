from copy import copy

from scripts.constants import *
from PgHelp import *
from scripts.Managers.IngameManagers.Inventory import Slot
from scripts.Entities.ABC.Building import Building
from scripts.Classes.Registry.EntityRegistry import EntityRegistry
from scripts.Managers.GameAssets import FUEL_WEIGHT, foundry_recipies
from math import sin


TEXTURE_SIZE = Vector(TILE_SIZE.x * 1.5, TILE_SIZE.y * 1.5)
TEXTURE_OFFSET = TEXTURE_SIZE * Vector(-0.5, -0.8)
TEXTURE_ACTIVE = load_texture("assets/entities/foundry/on.png", TEXTURE_SIZE)
TEXTURE_PASSIVE = load_texture("assets/entities/foundry/off.png", TEXTURE_SIZE)

HITBOX_SIZE = TEXTURE_SIZE * Vector(0.9, 0.6)
HITBOX_OFFSET = TEXTURE_SIZE * Vector(0.05, 0.4)

SOUND1 = pg.mixer.Sound("sound/pickaxe_1.mp3")
SOUND1.set_volume(0.5)
SOUND2 = pg.mixer.Sound("sound/ore_done.mp3")
SOUND2.set_volume(0.5)


class Foundry(Building, metaclass=EntityRegistry):

    def __init__(self, code, pos, parent):

        super().__init__(code, pos, parent, TEXTURE_PASSIVE, 200,
                         TEXTURE_OFFSET, "foundry", "pickaxe", forced_updating=True,
                         punch_sound=SOUND1, break_sound=SOUND2, ui_id="FoundryUI",
                         collider_hitbox_size=HITBOX_SIZE, collider_hitbox_offset=HITBOX_OFFSET)

        self.fuel_slot = Slot()
        self.ingredient_slot = Slot()
        self.result_slot = Slot()
        self.mold_slot = Slot()

        self.fuel_left = 0
        self.fuel_start_amount = 100
        self.progress_start = 10
        self.progress_left = 0
        self.currently_cooking = None

        self.starting_animation_counter_offset = self.parent.animation_counter % 30 + 1

    def drop_items(self):

        self.parent.drop_items(self.pos, self.item, 1)
        self.parent.drop_items(self.pos, self.fuel_slot.item_name, self.fuel_slot.item_amount)
        self.parent.drop_items(self.pos, self.ingredient_slot.item_name, self.ingredient_slot.item_amount)
        self.parent.drop_items(self.pos, self.result_slot.item_name, self.result_slot.item_amount)
        self.parent.drop_items(self.pos, self.mold_slot.item_name, self.mold_slot.item_amount)

    def insert(self, item_name, item_amount):

        if "mold" in item_name and self.mold_slot.can_fit(item_name, item_amount):
            self.mold_slot.append(item_name, item_amount)
        elif item_name in FUEL_WEIGHT and self.fuel_slot.can_fit(item_name, item_amount):
            self.fuel_slot.append(item_name, item_amount)
        elif self.ingredient_slot.can_fit(item_name, item_amount):
            self.ingredient_slot.append(item_name, item_amount)

    def can_insert(self, item_name, item_amount):

        if "mold" in item_name:
            return self.mold_slot.can_fit(item_name, item_amount)
        elif item_name in FUEL_WEIGHT:
            return self.fuel_slot.can_fit(item_name, item_amount)
        else:
            return self.ingredient_slot.can_fit(item_name, item_amount)

    def select_texture(self) -> pg.Surface:

        return TEXTURE_ACTIVE if self.fuel_left > 0 else TEXTURE_PASSIVE

    def _calculate_active_texture_size(self) -> Vector:

        return Vector(-sin(self.parent.animation_counter / self.anim_speed_val) * self.anim_val,
                      sin(self.parent.animation_counter / self.anim_speed_val) * self.anim_val)

    def update(self, preview_mode: bool = False):

        super().update(preview_mode)

        if self.ingredient_slot.item_amount > 0 and self.mold_slot.item_amount > 0:
            if self.fuel_slot.item_amount > 0 and self.fuel_left < 1 and self.fuel_slot.item_name in FUEL_WEIGHT:
                self.fuel_left = FUEL_WEIGHT[self.fuel_slot.item_name]
                self.fuel_start_amount = FUEL_WEIGHT[self.fuel_slot.item_name]
                self.fuel_slot.pop(1)
            if self.currently_cooking is None:
                recipe = foundry_recipies.find(self.ingredient_slot.item_name, self.mold_slot.item_name)
                if (not (recipe is None)) and self.fuel_left > 0 and self.result_slot.can_fit(recipe.result, 1):
                    self.currently_cooking = recipe.result
                    self.progress_left = recipe.weight
                    self.progress_start = recipe.weight
                    self.ingredient_slot.pop(1)

        if self.parent.animation_counter % 3 == 0:
            if self.fuel_left > 0:
                self.fuel_left -= 1
                if self.progress_left > 0:
                    self.progress_left -= 1
                    if self.progress_left < 1:
                        self.result_slot.append(self.currently_cooking, 1)
                        self.currently_cooking = None

        self.active = self.progress_left > 0 and self.fuel_left > 0

        if self.active:
            if self.parent.animation_counter % 30 - self.starting_animation_counter_offset == 0:
                self.summon_smoke(self.pos + self.texture_offset + TEXTURE_SIZE * Vector(0.35, 0) - Vector(8, 8), (16, 16))
                self.summon_smoke(self.pos + self.texture_offset + TEXTURE_SIZE * Vector(0.7, -0.1) - Vector(8, 8), (16, 16))

    def dumb(self) -> dict:

        return {
            "class": self.__class__.__name__,
            "pos": self.pos.as_list(),
            "fuel_slot": self.fuel_slot.dumb(),
            "ingredient_slot": self.ingredient_slot.dumb(),
            "mold_slot": self.mold_slot.dumb(),
            "result_slot": self.result_slot.dumb(),
            "progress_left": self.progress_left,
            "progress_start": self.progress_start,
            "currently_cooking": self.currently_cooking,
            "fuel_left": self.fuel_left,
            "fuel_start": self.fuel_start_amount
        }

    def load(self, data: dict):

        super().load(data)

        self.ingredient_slot.load(data["ingredient_slot"])
        self.fuel_slot.load(data["fuel_slot"])
        self.mold_slot.load(data["mold_slot"])
        self.result_slot.load(data["result_slot"])

        self.fuel_left = data["fuel_left"]
        self.fuel_start_amount = data["fuel_start"]
        self.progress_left = data["progress_left"]
        self.progress_start = data["progress_start"]
        self.currently_cooking = data["currently_cooking"]

        self.starting_animation_counter_offset = self.parent.animation_counter % 30
