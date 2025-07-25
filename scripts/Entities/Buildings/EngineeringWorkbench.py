from scripts.Managers.IngameManagers.Inventory import Slot, Inventory
from scripts.constants import *
from PgHelp import *
from scripts.Entities.ABC.Building import Building
from scripts.Classes.Registry.EntityRegistry import EntityRegistry

TEXTURE_SIZE = Vector(TILE_SIZE.x * 2, TILE_SIZE.y * 2)
TEXTURE = load_texture("assets/entities/engineering_workbench.png", TEXTURE_SIZE)
TEXTURE_OFFSET = Vector(-(TEXTURE_SIZE.x / 2), -(TEXTURE_SIZE.y / 6 * 5))
SOUND1 = pg.mixer.Sound("sound/pickaxe_1.mp3")
SOUND1.set_volume(0.5)
SOUND2 = pg.mixer.Sound("sound/ore_done.mp3")
SOUND2.set_volume(0.5)
COLLIDER_HITBOX_SIZE = TEXTURE_SIZE * Vector(0.9, 0.45)
COLLIDER_HITBOX_OFFSET = TEXTURE_SIZE * Vector(0.05, 0.55)
HITBOX_SIZE = TEXTURE_SIZE * Vector(0.9, 0.5)
HITBOX_OFFSET = TEXTURE_SIZE * Vector(0.05, 0.5)


class EngineeringWorkbench(Building, metaclass=EntityRegistry):

    def __init__(self, code, pos, parent):

        super().__init__(code, pos, parent, TEXTURE, 200, TEXTURE_OFFSET, "engineering_workbench", "pickaxe", 0, SOUND1, SOUND2, ui_id="EngineeringWorkbenchUI",
                         collider_hitbox_size=COLLIDER_HITBOX_SIZE, collider_hitbox_offset=COLLIDER_HITBOX_OFFSET, hitbox_offset=HITBOX_OFFSET, hitbox_size=HITBOX_SIZE)

        self.input_items = Inventory(self.parent, 6)
        self.output_item = Slot()

    def drop_items(self):

        super().drop_items()
        for name, amount in zip(self.input_items.n, self.input_items.a):
            self.parent.drop_items(self.pos, name, amount)
        self.parent.drop_items(self.pos, self.output_item.item_name, self.output_item.item_amount)

    def dumb(self) -> dict:

        return {
            "class": self.__class__.__name__,
            "pos": self.pos.as_tuple(),
            "input": self.input_items.dumb(),
            "output": self.output_item.dumb()
        }

    def load(self, data: dict):

        self.pos = from_iterable(data["pos"])
        self.input_items.load(data["input"])
        self.output_item.load(data["output"])

    def __repr__(self):

        return f"EngineeringWorkbench at {self.pos.as_tuple()}"
