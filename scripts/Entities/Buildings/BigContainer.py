from scripts.constants import *
from PgHelp import *
from scripts.Managers.IngameManagers.Inventory import Inventory
from scripts.Entities.ABC.Building import Building
from scripts.Classes.Registry.EntityRegistry import EntityRegistry


TEXTURE_SIZE = TILE_SIZE * Vector(2, 2)
TEXTURE_OFFSET = Vector(-(TEXTURE_SIZE.x / 2), -(TEXTURE_SIZE.y / 4 * 3))
TEXTURE = load_texture("assets/entities/container.png", TEXTURE_SIZE)
SOUND = pg.mixer.Sound("sound/axe.mp3")
SOUND.set_volume(0.5)
HITBOX_SIZE = TEXTURE_SIZE * Vector(0.7, 0.6)
HITBOX_OFFSET = TEXTURE_SIZE * Vector(0.15, 0.4)


class BigContainer(Building, metaclass=EntityRegistry):

    def __init__(self, code, pos, parent):

        super().__init__(code, pos, parent, TEXTURE, 100, TEXTURE_OFFSET, "big_container", "axe", 17, SOUND, ui_id="BigContainerUI",
                         collider_hitbox_size=HITBOX_SIZE, collider_hitbox_offset=HITBOX_OFFSET)
        self.inventory = Inventory(self, 40)

    def drop_items(self):

        super().drop_items()
        for item, amount in zip(self.inventory.n, self.inventory.a):
            self.parent.drop_items(self.pos, item, amount)

    def dumb(self) -> dict:

        return {
            "class": self.__class__.__name__,
            "pos": self.pos.as_tuple(),
            "inventory": self.inventory.dumb()
        }

    def load(self, data: dict):

        self.pos = from_iterable(data["pos"])
        self.inventory.load(data["inventory"])
