from scripts.constants import *
from PgHelp import *
from scripts.Managers.IngameManagers.Inventory import Slot
from scripts.Entities.ABC.Building import Building
from scripts.Entities.Particle import Particle
from random import randint
from scripts.Managers.GameAssets import crusher_recipies
from scripts.Classes.Registry.EntityRegistry import EntityRegistry
from scripts.Managers.GameAssets import PARTICLE_TEXTURES


TEXTURE_SIZE = TILE_SIZE * Vector(2, 2)
TEXTURE = load_texture("assets/entities/crusher.png", TEXTURE_SIZE)
TEXTURE_OFFSET = TEXTURE_SIZE * Vector(-0.5, -0.8)
HITBOX_SIZE = TEXTURE_SIZE * Vector(1, 0.55)
HITBOX_OFFSET = TEXTURE_SIZE * Vector(0, 0.45)
TOUCH_HITBOX_SIZE = TEXTURE_SIZE * Vector(0.8, 0.3)
TIUCH_HITBOX_OFFSET = TEXTURE_SIZE * Vector(0.1, 0.7)


class Crusher(Building, metaclass=EntityRegistry):

    def __init__(self, code, pos, parent):

        super().__init__(code, pos, parent, TEXTURE, 200, TEXTURE_OFFSET, "crusher", "pickaxe", 5,
                         ui_id="CrusherUI", hitbox_size=HITBOX_SIZE, hitbox_offset=HITBOX_OFFSET, forced_updating=True,
                         collider_hitbox_size=TOUCH_HITBOX_SIZE, collider_hitbox_offset=TIUCH_HITBOX_OFFSET)

        self.ing_slot = Slot()
        self.res_slot = Slot()

        self.max_progress = 0
        self.progress = 0
        self.cooking = [None, 0]
        self.particle_type = "copper"

        self.sound = pg.mixer.Sound("sound/crusher.mp3")
        self.sound.set_volume(0)

        #self.sound.play(-1)

    def cook(self, item_name, time, particle_type, item_amount):

        if self.ing_slot.item_amount > 0 and self.res_slot.can_fit(item_name, item_amount):
            self.ing_slot.pop(1)
            self.max_progress = time
            self.progress = 0
            self.cooking = [item_name, item_amount]
            self.particle_type = particle_type

    def draw(self):

        if self.do_draw:
            shake_offset = Vector(randint(1, 4), randint(1, 4)) if self.progress > 0 else Vector(0, 0)
            self.parent.screen.blit(self.select_texture(), (self.screen_pos + shake_offset).as_tuple())
            if self.touching: draw_brackets(self.parent.screen, self.rect)
            self.draw_secret_data()

    def update(self, preview_mode: bool = False):

        super().update(preview_mode)

        #if self.max_progress != 0:
        #    d = distance(self.pos, self.parent.player.pos)
        #    if d > TILE_SIZE.x * 10:
        #        volume = 0
        #    else:
        #        volume = (d / TILE_SIZE.x * 2) * 0.1
        #else:
        #    volume = 0

        #self.sound.set_volume(volume)

        if not preview_mode:

            if self.max_progress != 0:
                particle_pos = self.pos + Vector(randint(int(-self.texture_size.x / 2), int(self.texture_size.x / 4)), -self.texture_size.y / 4)
                particle_velocity = Vector(randint(-2, 2), randint(-5, -2))
                texture = PARTICLE_TEXTURES[self.particle_type]
                particle = Particle(self.parent.generate_id(), particle_pos, self.parent, particle_velocity, 20, texture)
                self.parent.particles.append(particle)

            if self.ing_slot.item_amount > 0 and self.max_progress == 0 and crusher_recipies.find(self.ing_slot.item_name):

                recipe = crusher_recipies.find(self.ing_slot.item_name)
                self.cook(recipe.result[0], recipe.time, recipe.particle_type, recipe.result[1])

            if self.parent.animation_counter % 3 == 0:

                if self.progress < self.max_progress:
                    self.progress += 1
                if self.progress >= self.max_progress and self.cooking[0]:
                    self.res_slot.append(self.cooking[0], self.cooking[1])
                    self.cooking[0] = None
                    self.max_progress = 0
                    self.progress = 0

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

    def __repr__(self):

        return f"Crusher ant {self.pos}: {self.ing_slot, self.res_slot, self.progress, self.max_progress}"
