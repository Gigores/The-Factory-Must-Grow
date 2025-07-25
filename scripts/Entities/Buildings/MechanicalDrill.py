from scripts.Managers.GameAssets import TILE_TO_ORE_TYPE
from scripts.Managers.IngameManagers.Inventory import Inventory, Slot
from scripts.Classes.Registry.EntityRegistry import EntityRegistry
from scripts.Entities.ABC.Building import Building
from scripts.Entities.Particle import Particle
from scripts.constants import *
from random import randint
from copy import deepcopy
from math import sin
from scripts.Managers.GameAssets import *


TEXTURE_SIZE = TILE_SIZE * Vector(1, 2)
TEXTURE_OFFSET = TEXTURE_SIZE * Vector(-0.5, -0.85)
TEXTURE1 = load_texture("assets/entities/mechanical_drill/a.png", TEXTURE_SIZE)
TEXTURE2 = load_texture("assets/entities/mechanical_drill/a2.png", TEXTURE_SIZE)
HITBOX_SIZE = TEXTURE_SIZE * Vector(0.9, 0.4)
HITBOX_OFFSET = TEXTURE_SIZE * Vector(0.05, 0.55)


TEXTURES_DRILL = [
    load_texture("assets/entities/mechanical_drill/b1.png", TEXTURE_SIZE),
    load_texture("assets/entities/mechanical_drill/b2.png", TEXTURE_SIZE),
    load_texture("assets/entities/mechanical_drill/b3.png", TEXTURE_SIZE),
]


class MechanicalDrill(Building, metaclass=EntityRegistry):

    def __init__(self, code, pos, parent):

        super().__init__(code, pos, parent, TEXTURE2, 100, TEXTURE_OFFSET, "mechanical_drill", "pickaxe", hitbox_size=HITBOX_SIZE, hitbox_offset=HITBOX_OFFSET, collider_hitbox_size=HITBOX_SIZE, collider_hitbox_offset=HITBOX_OFFSET, ui_id="MechanicalDrillUI", forced_updating=True)
        self.anim_speed_val = 40
        self.current_drill = 0
        self.current_ore = None
        self.inventory = Inventory(self, 9)
        self.fuel_slot = Slot()
        self.fuel_left = 0
        self.fuel_start_amount = 0
        self.progress = 0
        self.beggining_progress = 0

    def select_texture(self) -> pg.Surface:

        return TEXTURE2 if self.active else TEXTURE1

    def draw(self):

        if self.do_draw:
            if self.active:
                pos = self.screen_pos + Vector(randint(-int(TILE_SIZE.x / 64), int(TILE_SIZE.x / 64)), randint(-int(TILE_SIZE.y / 64), int(TILE_SIZE.y / 64)))
            else:
                pos = self.screen_pos
            texture = self.select_texture()

            drill_pos = deepcopy(pos) + (Vector(0, sin(self.parent.animation_counter / self.anim_speed_val) * (TILE_SIZE.y / 12) + (TILE_SIZE.y / 12)) if self.active else Vector(0, 0))
            screen.blit(TEXTURES_DRILL[self.current_drill // len(TEXTURES_DRILL)], drill_pos.as_tuple())

            screen.blit(texture, pos.as_tuple())

            if self.touching: draw_brackets(screen, self.rect)
            self.draw_secret_data()

    def update(self, preview_mode: bool = False):

        super().update(preview_mode)

        if self.fuel_slot.item_amount > 0 and self.fuel_left == 0 and self.fuel_slot.item_name in FUEL_WEIGHT.keys() and self.current_ore:
            self.fuel_start_amount = FUEL_WEIGHT[self.fuel_slot.item_name]
            self.fuel_left = FUEL_WEIGHT[self.fuel_slot.item_name]
            self.fuel_slot.pop(1)
            if self.progress == 0:
                self.progress = ORE_TYPE_TO_HP[ITEM_TO_ORE_TYPE[self.current_ore]]
                self.beggining_progress = ORE_TYPE_TO_HP[ITEM_TO_ORE_TYPE[self.current_ore]]

        if self.parent.animation_counter % 3 == 0:
            if self.progress > 0 and self.active and self.inventory.can_fit(self.current_ore, 1):
                self.progress -= 0.5
                if self.progress <= 0:
                    self.progress = ORE_TYPE_TO_HP[ITEM_TO_ORE_TYPE[self.current_ore]]
                    self.beggining_progress = ORE_TYPE_TO_HP[ITEM_TO_ORE_TYPE[self.current_ore]]
                    self.inventory.append(self.current_ore, 1)
            if self.fuel_left > 0: self.fuel_left -= 1

        self.active = self.fuel_left > 0

        if not preview_mode:

            if not self.current_ore:
                if self.parent.world.data[int(self.pos.x // TILE_SIZE.x)][int(self.pos.y // TILE_SIZE.y)] in TILE_TO_ORE_TYPE.keys():
                    self.current_ore = TILE_TO_ORE_TYPE[self.parent.world.data[int(self.pos.x // TILE_SIZE.x)][int(self.pos.y // TILE_SIZE.y)]]

            if self.active:
                particle_pos = self.pos + Vector(randint(-int(TILE_SIZE.x / 8), int(TILE_SIZE.x / 8)) - TILE_SIZE.x / 8, 0 + TILE_SIZE.x / 8)
                particle_velocity = Vector(randint(-2, 2), randint(-5, -2))
                texture = PARTICLE_TEXTURES.get(ITEM_TO_ORE_TYPE[self.current_ore], PARTICLE_TEXTURES["stone"])
                particle = Particle(self.parent.generate_id(), particle_pos, self.parent, particle_velocity, 20, texture)
                self.parent.particles.append(particle)

    def drop_items(self):

        super().drop_items()
        self.parent.drop_items(self.pos, self.fuel_slot.item_name, self.fuel_slot.item_amount)
        for item, amount in zip(self.inventory.n, self.inventory.a):
            self.parent.drop_items(self.pos, item, amount)

    def dumb(self) -> dict:

        return {
            "class": self.__class__.__name__,
            "pos": self.pos.as_tuple(),
            "inv": self.inventory.dumb(),
            "fuel_slot": self.fuel_slot.dumb(),
            "fuel_left": self.fuel_left,
            "fuel_start": self.fuel_start_amount,
            "progress": self.progress,
            "progress_start": self.beggining_progress,
            "ore": self.current_ore
        }

    def load(self, data: dict):

        self.pos = from_iterable(data["pos"])
        self.inventory.load(data["inv"])
        self.fuel_slot.load(data["fuel_slot"])
        self.fuel_left = data["fuel_left"]
        self.fuel_start_amount = data["fuel_start"]
        self.progress = data["progress"]
        self.beggining_progress = data["progress_start"]
        self.current_ore = data["ore"]
