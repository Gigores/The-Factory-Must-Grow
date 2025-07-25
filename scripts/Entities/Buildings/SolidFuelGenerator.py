from copy import copy

from scripts.constants import *
from PgHelp import *
from scripts.Entities.ABC.ElectricNode import ElectricNode
from scripts.Managers.IngameManagers.Inventory import Slot
from scripts.Classes.Registry.EntityRegistry import EntityRegistry
from scripts.Managers.GameAssets import FUEL_WEIGHT


TEXTURE_SIZE = TILE_SIZE * Vector(2, 2)
TEXTURE_OFFSET = TEXTURE_SIZE * Vector(-0.5, -1)
CONNECTION_OFFSET = TEXTURE_SIZE / Vector(-3.555555555555555556, -5.3333333333333333333333333333333)
TEXTURE = load_texture("assets/entities/solid_fuel_electric_generator.png", TEXTURE_SIZE)
TEXTURE_ON = load_texture("assets/entities/solid_fuel_electric_generator_on.png", TEXTURE_SIZE)
COLLIDER_HITBOX_SIZE = TEXTURE_SIZE * Vector(0.95, 0.4)
COLLIDER_HITBOX_OFFSET = TEXTURE_SIZE * Vector(0.025, 0.6)

SOUND1 = pg.mixer.Sound("sound/pickaxe_1.mp3")
SOUND1.set_volume(0.5)
SOUND2 = pg.mixer.Sound("sound/ore_done.mp3")
SOUND2.set_volume(0.5)


class SolidFuelGenerator(ElectricNode, metaclass=EntityRegistry):

    def __init__(self, code, pos, parent):

        super().__init__(code, pos, parent, TEXTURE, 50, TEXTURE_OFFSET,
                         "solid_fuel_generator", "pickaxe", ui_id="SolidFuelGeneratorUI",
                         wire_connection_offset=CONNECTION_OFFSET, collider_hitbox_size=COLLIDER_HITBOX_SIZE,
                         collider_hitbox_offset=COLLIDER_HITBOX_OFFSET, network_weight=500_000,
                         punch_sound=SOUND1, break_sound=SOUND2)

        self.fuel_slot = Slot()

        self.fuel_left = 0
        self.fuel_total = 0
        self.anim_speed_val = 50

        self.starting_animation_counter_offset = 0

    def select_texture(self) -> pg.Surface:

        return TEXTURE_ON if self.fuel_left > 0 else TEXTURE

    def update(self, preview_mode: bool = False):

        super().update(preview_mode)

        self.network_weight = 500_000 * int(self.fuel_left > 0)
        was_asctive = copy(self.active)
        self.active = self.fuel_left > 0

        if self.parent.animation_counter % 3 == 0:
            if self.fuel_left > 0:
                self.fuel_left -= 1
                if self.fuel_left <= 0:
                    self.fuel_total = 0
                    self.fuel_left = 0

        if self.fuel_left == 0 and self.fuel_slot.item_amount > 0:
            if self.fuel_slot.item_name in FUEL_WEIGHT:
                self.fuel_left = self.fuel_total = FUEL_WEIGHT[self.fuel_slot.item_name]
                self.fuel_slot.pop(1)

        if was_asctive and was_asctive != self.active:
            self.starting_animation_counter_offset = self.parent.animation_counter % 30

        if self.active:
            if self.parent.animation_counter % 30 - self.starting_animation_counter_offset == 0:
                self.summon_smoke(self.pos + self.texture_offset + TEXTURE_SIZE * Vector(0.5, 0.3) - Vector(8, 8), (16, 16))
                self.summon_smoke(self.pos + self.texture_offset + TEXTURE_SIZE * Vector(0.75, 0.3) - Vector(8, 8), (16, 16))

    def dumb(self) -> dict:

        return {
            "class": self.__class__.__name__,
            "code": self.code,
            "pos": self.pos.as_tuple(),
            "fuel_left": self.fuel_left,
            "fuel_total": self.fuel_total,
            "fuel_slot": self.fuel_slot.dumb()
        }

    def load(self, data: dict):

        self.pos = from_iterable(data["pos"])
        self.code = data["code"]
        self.fuel_left = data["fuel_left"]
        self.fuel_total = data["fuel_total"]
        self.fuel_slot.load(data["fuel_slot"])

        self.starting_animation_counter_offset = self.parent.animation_counter % 30
