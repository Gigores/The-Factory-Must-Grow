from scripts.constants import *
from scripts.Managers.IngameManagers.Inventory import Inventory
from scripts.Entities.ABC.Building import Building
from scripts.Managers.GameAssets import items
from scripts.Classes.Registry.EntityRegistry import EntityRegistry


class Table(Building, metaclass=EntityRegistry):

    def __init__(self, code, pos, parent):

        texture_size = TILE_SIZE * Vector(1.5, 1.5)
        texture = load_texture("assets/entities/table.png", texture_size)
        texture_offset = texture_size * Vector(-0.5, -0.8)
        sound = pg.mixer.Sound("sound/axe.mp3")
        sound.set_volume(0.5)
        hitbox_offset = texture_size * Vector(0, 0.5)
        hitbox_size = texture_size * Vector(1, 0.5)
        super().__init__(code, pos, parent, texture, 10, texture_offset, "table", "axe", 14,
                         ui_id="TableUI", punch_sound=sound, collider_hitbox_size=hitbox_size, collider_hitbox_offset=hitbox_offset)
        self.inventory = Inventory(self.parent, 3)
        self.inv_offset = texture_size * Vector(0.05, 0.3)
        self.item_size = texture_size * Vector(0.3, 0.3)

    def draw(self):

        if self.do_draw:
            screen.blit(self.texture, self.screen_pos.as_tuple())
            if self.touching: draw_brackets(self.parent.screen, self.rect)
            for n, (item_name, item_amount) in enumerate(zip(self.inventory.n, self.inventory.a)):
                if item_name:
                    stack_size = items[item_name].stack_size
                    if items[item_name].stack_size == 1:
                        pos = self.screen_pos + self.inv_offset + (self.item_size + Vector(0, 20)) * Vector(n, 0)
                        texture = pg.transform.scale(items[item_name].texture, self.item_size.as_tuple())
                        screen.blit(texture, pos.as_tuple())
                    else:
                        for i in range(item_amount // int(stack_size / 4) + int(item_amount < stack_size)):
                            pos = self.screen_pos + self.inv_offset + (self.item_size + Vector(0, 20)) * Vector(n, 0) + Vector(0, 10 * -i)
                            texture = pg.transform.scale(items[item_name].texture, self.item_size.as_tuple())
                            screen.blit(texture, pos.as_tuple())
            self.draw_secret_data()

    def drop_items(self):

        super().drop_items()
        for name, amount in zip(self.inventory.n, self.inventory.a):
            self.parent.drop_items(self.pos, name, amount)

    def dumb(self) -> dict:

        return {
            "class": self.__class__.__name__,
            "pos": self.pos.as_list(),
            "inventory": self.inventory.dumb()
        }

    def load(self, data: dict):

        self.pos = from_iterable(data["pos"])
        self.inventory.load(data["inventory"])
