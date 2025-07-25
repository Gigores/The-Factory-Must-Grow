from scripts.constants import *
from PgHelp import *
from scripts.Managers.IngameManagers.Inventory import Slot
from scripts.Entities.ABC.Building import Building
from scripts.Managers.GameAssets import centrifuge_recipies
from scripts.Classes.Registry.EntityRegistry import EntityRegistry


TEXTURE_SIZE = TILE_SIZE * Vector(3, 3)
TEXTURE_OFFSET = TEXTURE_SIZE * Vector(-0.5, -0.8)
TOUCH_HITBOX_SIZE = TEXTURE_SIZE * Vector(0.7, 0.27)
TOUCH_HITBOX_OFFSET = TEXTURE_SIZE * Vector(0.13, 0.7)
HITBOX_SIZE = TEXTURE_SIZE * Vector(0.77, 0.6)
HITBOX_OFFSET = TEXTURE_SIZE * Vector(0.1, 0.4)
TEXTURES = [
    load_texture("assets/entities/magnetic_centrifuge/0.png", TEXTURE_SIZE),
    load_texture("assets/entities/magnetic_centrifuge/1.png", TEXTURE_SIZE),
    load_texture("assets/entities/magnetic_centrifuge/2.png", TEXTURE_SIZE),
    load_texture("assets/entities/magnetic_centrifuge/3.png", TEXTURE_SIZE),
]


class MagneticCentrifuge(Building, metaclass=EntityRegistry):

    def __init__(self, code, pos, parent):

        super().__init__(code, pos, parent, TEXTURES, 300, TEXTURE_OFFSET, "magnetic_centrifuge", "pickaxe", 7,
                         collider_hitbox_offset=TOUCH_HITBOX_OFFSET, collider_hitbox_size=TOUCH_HITBOX_SIZE, forced_updating=True,
                         hitbox_offset=HITBOX_OFFSET, hitbox_size=HITBOX_SIZE, ui_id="MagneticCentrifugeUI")
        self.animation_frame = 0
        self.anim_val = 2
        self.anim_speed_val = 10

        self.ing_slot = Slot()
        self.res1_slot = Slot()
        self.res2_slot = Slot()

        self.max_progress = 0
        self.progress = 0
        self.cooking = [[None, 0], [None, 0]]

    def select_texture(self) -> pg.Surface:

        return self.texture[self.animation_frame]

    def cook(self, recipe):

        if self.ing_slot.item_amount > 0 and self.res1_slot.can_fit(recipe.result1[0], recipe.result1[1]) and \
                self.res2_slot.can_fit(recipe.result2[0], recipe.result2[1]):
            self.ing_slot.pop(1)
            self.max_progress = recipe.time
            self.progress = 0
            self.cooking = [[recipe.result1[0], recipe.result1[1]], [recipe.result2[0], recipe.result2[1]]]

    def update(self, preview_mode: bool = False):

        super().update(preview_mode)

        self.active = not self.max_progress == 0

        if self.active: self.animation_frame = self.parent.animation_counter // 8 % 4

        if self.ing_slot.item_amount > 0 and self.max_progress == 0 and centrifuge_recipies.find(self.ing_slot.item_name):

            self.cook(centrifuge_recipies.find(self.ing_slot.item_name))

        if self.parent.animation_counter % 3 == 0:

            if self.progress < self.max_progress:
                self.progress += 1
            if self.progress >= self.max_progress and self.cooking[0][0]:
                self.res1_slot.append(self.cooking[0][0], self.cooking[0][1])
                self.res2_slot.append(self.cooking[1][0], self.cooking[1][1])
                self.cooking[0][0] = None
                self.cooking[1][0] = None
                self.max_progress = 0
                self.progress = 0

    def drop_items(self):

        super().drop_items()
        self.parent.drop_items(self.pos, self.ing_slot.item_name, self.ing_slot.item_amount)
        self.parent.drop_items(self.pos, self.res1_slot.item_name, self.res1_slot.item_amount)
        self.parent.drop_items(self.pos, self.res2_slot.item_name, self.res2_slot.item_amount)

    def dumb(self) -> dict:

        return {
            "class": self.__class__.__name__,
            "pos": self.pos.as_list(),
            "slot1": self.ing_slot.dumb(),
            "slot2": self.res1_slot.dumb(),
            "slot3": self.res2_slot.dumb(),
            "progress": self.progress,
            "max_progress": self.max_progress,
            "cooking": self.cooking,
        }

    def load(self, data: dict):

        self.pos = from_iterable(data["pos"])
        self.ing_slot.load(data["slot1"])
        self.res1_slot.load(data["slot2"])
        self.res2_slot.load(data["slot3"])
        self.progress = data["progress"]
        self.max_progress = data["max_progress"]
        self.cooking = data["cooking"]
