from scripts.Managers.IngameManagers.Inventory import Slot
from scripts.Managers.IngameManagers.InventoryLiquids import InventoryTank
from scripts.Classes.Registry.EntityRegistry import EntityRegistry
from scripts.Entities.ABC.Building import Building
from scripts.constants import *
from scripts.Managers.GameAssets import liquids


TEXTURE_SIZE = TILE_SIZE * Vector(2, 2)
TEXTURE = load_texture("assets/entities/fluid_tank.png", TEXTURE_SIZE)
TEXTURE_OFFSET = TEXTURE_SIZE * Vector(-0.5, -0.7)
HITBOX_SIZE = TEXTURE_SIZE * Vector(0.8, 0.3)
HITBOX_OFFSET = TEXTURE_SIZE * Vector(0.1, 0.6)

SOUND1 = pg.mixer.Sound("sound/pickaxe_1.mp3")
SOUND1.set_volume(0.5)
SOUND2 = pg.mixer.Sound("sound/ore_done.mp3")
SOUND2.set_volume(0.5)


class FluidTank(Building, metaclass=EntityRegistry):

    def __init__(self, code, pos, parent):

        super().__init__(code, pos, parent, TEXTURE, 200, TEXTURE_OFFSET,
                         "fluid_tank", "pickaxe",
                         collider_hitbox_offset=HITBOX_OFFSET, collider_hitbox_size=HITBOX_SIZE, ui_id="GenericTankUI",
                         punch_sound=SOUND1, break_sound=SOUND2)

        self.tank = InventoryTank(100)
        self.input_slot = Slot()
        self.output_slot = Slot()

    def update(self, preview_mode: bool = False):

        super().update(preview_mode)

        self._handle_tank_interraction(self.tank, self.input_slot, self.output_slot)

    def dumb(self) -> dict:

        return {
            "class": self.__class__.__name__,
            "pos": self.pos.as_tuple(),
            "input_slot": self.input_slot.dumb(),
            "output_slot": self.output_slot.dumb(),
            "tank": self.tank.dumb()
        }

    def load(self, data: dict):

        self.pos = from_iterable(data["pos"])
        self.input_slot.load(data["input_slot"])
        self.output_slot.load(data["output_slot"])
        self.tank.load(data["tank"])
