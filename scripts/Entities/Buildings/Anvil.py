from scripts.constants import *
from PgHelp import *
from scripts.Entities.ABC.Building import Building
from scripts.Managers.IngameManagers.Inventory import Slot
from scripts.Classes.Registry.EntityRegistry import EntityRegistry

TEXTURE_SIZE = Vector(TILE_SIZE.x * 1, TILE_SIZE.y * 1)
TEXTURE = load_texture("assets/entities/anvil.png", TEXTURE_SIZE)
TEXTURE_OFFSET = Vector(-(TEXTURE_SIZE.x / 2), -(TEXTURE_SIZE.y / 6 * 5))
SOUND = pg.mixer.Sound("sound/pickaxe_1.mp3")
SOUND.set_volume(0.5)
HITBOX_SIZE = TEXTURE_SIZE * Vector(0.94, 0.4)
HITBOX_OFFSET = TEXTURE_SIZE * Vector(0.04, 0.6)


class Anvil(Building, metaclass=EntityRegistry):

    def __init__(self, code, pos, parent):

        super().__init__(code, pos, parent, TEXTURE, 400, TEXTURE_OFFSET, "anvil", "pickaxe", 4, SOUND, ui_id="AnvilUI",
                         collider_hitbox_size=HITBOX_SIZE, collider_hitbox_offset=HITBOX_OFFSET)
        self.ingredient_slot = Slot()
        self.result_slot = Slot()

    def drop_items(self):

        super().drop_items()
        self.parent.drop_items(self.pos, self.ingredient_slot.item_name, self.ingredient_slot.item_amount)
        self.parent.drop_items(self.pos, self.result_slot.item_name, self.result_slot.item_amount)

    def dumb(self) -> dict:

        return {
            "class": self.__class__.__name__,
            "pos": self.pos.as_tuple(),
            "ingridient_slot": self.ingredient_slot.dumb(),
            "result_slot": self.result_slot.dumb(),
        }

    def load(self, data: dict):

        super().load(data)
        self.ingredient_slot.load(data["ingridient_slot"])
        self.result_slot.load(data["result_slot"])
