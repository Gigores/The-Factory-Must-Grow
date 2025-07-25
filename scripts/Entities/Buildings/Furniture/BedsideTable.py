from scripts.constants import *
from scripts.Managers.IngameManagers.Inventory import Inventory
from scripts.Entities.ABC.Building import Building
from scripts.Classes.Registry.EntityRegistry import EntityRegistry


class BedsideTable(Building, metaclass=EntityRegistry):

    def __init__(self, code, pos, parent):

        texture_size = TILE_SIZE
        texture = load_texture("assets/entities/bedside_table.png", texture_size)
        texture_offset = texture_size * Vector(-0.5, -0.8)
        sound = pg.mixer.Sound("sound/axe.mp3")
        sound.set_volume(0.5)
        touch_hitbox_size = texture_size * Vector(0.5, 0.4)
        touch_hitbox_offset = texture_size * Vector(0.25, 0.6)
        hitbox_size = texture_size * Vector(0.5, 0.7)
        hitbox_offset = texture_size * Vector(0.25, 0.3)

        super().__init__(code, pos, parent, texture, 1, texture_offset, "bedside_table", "axe",
                         15, punch_sound=sound, hitbox_size=hitbox_size, hitbox_offset=hitbox_offset,
                         collider_hitbox_size=touch_hitbox_size, collider_hitbox_offset=touch_hitbox_offset, ui_id="BedsideTableUI")

        self.inventory = Inventory(self.parent, 5)

    def drop_items(self):

        super().drop_items()
        for item, amount in zip(self.inventory.n, self.inventory.a):
            self.parent.drop_items(self.pos, item, amount)

    def dumb(self) -> dict:

        return {
            "class": self.__class__.__name__,
            "pos": self.pos.as_list(),
            "inventory": self.inventory.dumb()
        }

    def load(self, data: dict):

        self.pos = from_iterable(data["pos"])
        self.inventory.load(data["inventory"])
