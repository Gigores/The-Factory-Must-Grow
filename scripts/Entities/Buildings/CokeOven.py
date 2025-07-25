from scripts.constants import *
from PgHelp import *
from scripts.Managers.IngameManagers.Inventory import Slot
from scripts.Entities.ABC.Building import Building
from scripts.Entities.Particle import Particle
from random import randint
from scripts.Managers.GameAssets import coke_oven_recipies
from scripts.Classes.Registry.EntityRegistry import EntityRegistry
from math import sin


TEXTURE_SIZE = TILE_SIZE * Vector(2, 3)
TEXTURE1 = load_texture("assets/entities/coke_oven/off.png", TEXTURE_SIZE)
TEXTURE2 = load_texture("assets/entities/coke_oven/on.png", TEXTURE_SIZE)
TEXTURE_OFFSET = TEXTURE_SIZE * Vector(-0.5, -0.8)
HITBOX_SIZE = TEXTURE_SIZE * Vector(1, 0.55)
HITBOX_OFFSET = TEXTURE_SIZE * Vector(0, 0.45)
TOUCH_HITBOX_SIZE = TEXTURE_SIZE * Vector(0.8, 0.3)
TIUCH_HITBOX_OFFSET = TEXTURE_SIZE * Vector(0.1, 0.7)


class CokeOven(Building, metaclass=EntityRegistry):

    def __init__(self, code, pos, parent):

        super().__init__(code, pos, parent, TEXTURE1, 200, TEXTURE_OFFSET, "coke_oven", "pickaxe", 5,
                         ui_id="CokeOvenUI", hitbox_size=HITBOX_SIZE, hitbox_offset=HITBOX_OFFSET, forced_updating=True,
                         collider_hitbox_size=TOUCH_HITBOX_SIZE, collider_hitbox_offset=TIUCH_HITBOX_OFFSET)

        self.ing_slot = Slot()
        self.res_slot = Slot()

        self.max_progress = 0
        self.progress = 0
        self.cooking = [None, 0]
        self.particle_type = "copper"

        self.starting_animation_counter_offset = 0

        #self.sound.play(-1)

    def cook(self, item_name, time, item_amount):

        if self.ing_slot.item_amount > 0 and self.res_slot.can_fit(item_name, item_amount):
            self.ing_slot.pop(1)
            self.max_progress = time
            self.progress = 0
            self.cooking = [item_name, item_amount]

    def select_texture(self) -> pg.Surface:

        return TEXTURE2 if self.progress > 0 else TEXTURE1

    def draw(self):

        if self.do_draw:
            texture = self.select_texture()
            new_width = texture.get_width() + ((sin(self.parent.animation_counter / 20) * 12) if self.progress > 0 else 0)
            new_height = texture.get_height() + (((sin(self.parent.animation_counter / 20) + 0.5) * 12) if self.progress > 0 else 0)
            animation_offset = Vector((texture.get_width() - new_width) / 2, texture.get_height() - new_height)
            new_texture = pg.transform.scale(texture, (new_width, new_height))
            self.parent.screen.blit(new_texture, (self.screen_pos + animation_offset).as_tuple())
            if self.touching: draw_brackets(self.parent.screen, self.rect)
            self.draw_secret_data()

    def update(self, preview_mode: bool = False):

        super().update(preview_mode)

        was_active = self.progress > 0

        #if self.max_progress != 0:
        #    d = distance(self.pos, self.parent.player.pos)
        #    if d > TILE_SIZE.x * 10:
        #        volume = 0
        #    else:
        #        volume = (d / TILE_SIZE.x * 2) * 0.1
        #else:
        #    volume = 0

        #self.sound.set_volume(volume)

        if self.ing_slot.item_amount > 0 and self.max_progress == 0 and coke_oven_recipies.find(self.ing_slot.item_name):

            recipe = coke_oven_recipies.find(self.ing_slot.item_name)
            self.cook(recipe.result[0], recipe.time, recipe.result[1])

        if self.parent.animation_counter % 3 == 0:

            if self.progress < self.max_progress:
                self.progress += 1
            if self.progress >= self.max_progress and self.cooking[0]:
                self.res_slot.append(self.cooking[0], self.cooking[1])
                self.cooking[0] = None
                self.max_progress = 0
                self.progress = 0

        if was_active and self.progress < 1:
            self.starting_animation_counter_offset = self.parent.animation_counter % 30

        if self.progress > 0:
            if self.parent.animation_counter % 30 - self.starting_animation_counter_offset == 0:
                self.summon_smoke(self.pos + self.texture_offset + TEXTURE_SIZE * Vector(0.25, -0.1) - Vector(32, 32), (64, 64))

    def drop_items(self):

        super().drop_items()
        self.parent.drop_items(self.pos, self.ing_slot.item_name, self.ing_slot.item_amount)
        self.parent.drop_items(self.pos, self.res_slot.item_name, self.res_slot.item_amount)

    def dumb(self) -> dict:

        return {
            "class": self.__class__.__name__,
            "pos": self.pos.as_tuple(),
            "ingridient_slot": self.ing_slot.dumb(),
            "result_slot": self.res_slot.dumb(),
            "progress": self.progress,
            "progress_max": self.max_progress
        }

    def load(self, data: dict):

        super().load(data)
        self.ing_slot.load(data["ingridient_slot"])
        self.res_slot.load(data["result_slot"])
        self.progress = data["progress"]
        self.max_progress = data["progress_max"]

        self.starting_animation_counter_offset = self.parent.animation_counter % 30

    def __repr__(self):

        return f"Crusher ant {self.pos}: {self.ing_slot, self.res_slot, self.progress, self.max_progress}"
