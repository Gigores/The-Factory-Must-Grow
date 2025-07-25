from scripts.Managers.GameAssets import FUEL_WEIGHT
from scripts.constants import *
from PgHelp import *
from random import randint
from scripts.Managers.IngameManagers.Inventory import Slot
from scripts.Entities.ABC.Building import Building
from scripts.Entities.Particle import Particle
from scripts.Classes.Registry.EntityRegistry import EntityRegistry
from copy import copy


TEXTURE_SIZE = TILE_SIZE * Vector(4, 4)
TEXTURE_OFFSET = TEXTURE_SIZE * Vector(-0.5, -0.9)
TOUCH_HITBOX_SIZE = TEXTURE_SIZE * Vector(0.7, 0.3)
TOUCH_HITBOX_OFFSET = TEXTURE_SIZE * Vector(0.15, 0.7)
HITBOX_SIZE = TEXTURE_SIZE * Vector(0.8, 0.8)
HITBOX_OFFSET = TEXTURE_SIZE * Vector(0.1, 0.2)
TEXTURES = [
    load_texture("assets/entities/blast_furnace.png", TEXTURE_SIZE),
    load_texture("assets/entities/blast_furnace_active.png", TEXTURE_SIZE),
]
AVILABLE_FUEL = ("coking_coal",)
SOUND1 = pg.mixer.Sound("sound/pickaxe_1.mp3")
SOUND1.set_volume(0.5)
SOUND2 = pg.mixer.Sound("sound/ore_done.mp3")
SOUND2.set_volume(0.5)


class BlastFurnace(Building, metaclass=EntityRegistry):

    def __init__(self, code, pos, parent):

        super().__init__(code, pos, parent, TEXTURES, 800, TEXTURE_OFFSET, "blast_furnace", "pickaxe", 6,
                         collider_hitbox_offset=TOUCH_HITBOX_OFFSET, collider_hitbox_size=TOUCH_HITBOX_SIZE, punch_sound=SOUND1, break_sound=SOUND2,
                         hitbox_size=HITBOX_SIZE, hitbox_offset=HITBOX_OFFSET, ui_id="BlastFurnaceUI", forced_updating=True)

        self.eng1_slot = Slot()
        self.eng2_slot = Slot()
        self.fuel_slot = Slot()
        self.res_slot = Slot()
        self.fuel_left = 0
        self.progress_left = 0
        self.fuel_start_amount = 0

        self.starting_animation_counter_offset = 0

    def select_texture(self) -> pg.Surface:

        return self.texture[int(self.active)]

    def insert(self, item_name: str, item_amount: int):

        if item_name in AVILABLE_FUEL:
            self.fuel_slot.append(item_name, item_amount)
        elif item_name == "coal":
            self.eng1_slot.append(item_name, item_amount)
        elif item_name == "crushed_refined_raw_iron":
            self.eng2_slot.append(item_name, item_amount)

    def can_insert(self, item_name: str, item_amount: int) -> bool:

        if item_name in AVILABLE_FUEL:
            return self.fuel_slot.can_fit(item_name, item_amount)
        elif item_name == "coal":
            return self.eng1_slot.can_fit(item_name, item_amount)
        elif item_name == "crushed_refined_raw_iron":
            return self.eng2_slot.can_fit(item_name, item_amount)

    def update(self, preview_mode: bool = False):

        super().update(preview_mode)

        if self.eng2_slot.contain("crushed_refined_raw_iron", 1) and self.eng1_slot.contain("coal", 1) \
                and self.res_slot.can_fit("cast_iron_ingot", 1) and self.progress_left <= 0:
            if self.fuel_slot.item_name in AVILABLE_FUEL and self.fuel_left <= 0 :
                self.fuel_left = FUEL_WEIGHT[self.fuel_slot.item_name]
                self.fuel_start_amount = FUEL_WEIGHT[self.fuel_slot.item_name]
                self.fuel_slot.pop(1)
            if self.fuel_left > 0:
                self.eng2_slot.pop(1)
                self.eng1_slot.pop(1)
                self.progress_left = 2400

        if self.fuel_left > 0 and self.parent.animation_counter % 1 == 0:
            self.fuel_left -= 1
            if self.progress_left > 0:
                self.progress_left -= 1
                if self.progress_left <= 0:
                    self.res_slot.append("cast_iron_ingot", 1)

        was_asctive = copy(self.active)
        self.active = self.fuel_left > 0

        if was_asctive and was_asctive != self.active:
            self.starting_animation_counter_offset = self.parent.animation_counter % 30

        if self.active:
            if self.parent.animation_counter % 30 - self.starting_animation_counter_offset == 0:
                self.summon_smoke(self.pos + self.texture_offset + TEXTURE_SIZE * Vector(0.25, 0) - Vector(32, 32), (64, 64))

    def drop_items(self):

        super().drop_items()
        self.parent.drop_items(self.pos, self.fuel_slot.item_name, self.fuel_slot.item_amount)
        self.parent.drop_items(self.pos, self.eng1_slot.item_name, self.eng1_slot.item_amount)
        self.parent.drop_items(self.pos, self.eng2_slot.item_name, self.eng2_slot.item_amount)
        self.parent.drop_items(self.pos, self.res_slot.item_name, self.res_slot.item_amount)

    def dumb(self) -> dict:

        return {
            "class": self.__class__.__name__,
            "pos": self.pos.as_list(),
            "slot1": self.eng1_slot.dumb(),
            "slot2": self.eng2_slot.dumb(),
            "slot3": self.fuel_slot.dumb(),
            "slot4": self.res_slot.dumb(),
            "fuel_left": self.fuel_left,
            "fuel_start": self.fuel_start_amount,
            "progress_left": self.progress_left,
        }

    def load(self, data: dict):

        super().load(data)

        self.eng1_slot.load(data["slot1"])
        self.eng2_slot.load(data["slot2"])
        self.fuel_slot.load(data["slot3"])
        self.res_slot.load(data["slot4"])
        self.fuel_left = data["fuel_left"]
        self.fuel_start_amount = data["fuel_start"]
        self.progress_left = data["progress_left"]

        self.starting_animation_counter_offset = self.parent.animation_counter % 30
