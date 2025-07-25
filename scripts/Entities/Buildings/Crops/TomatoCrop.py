from scripts.constants import *
from scripts.Entities.ABC.Crop import Crop
from random import randint
from scripts.Classes.Registry.EntityRegistry import EntityRegistry


class TomatoCrop(Crop, metaclass=EntityRegistry):

    def __init__(self, code, pos, parent):

        texture_size = TILE_SIZE * Vector(1, 1.5)

        textures = (
            load_texture("assets/entities/crops/tomato1.png", texture_size),
            load_texture("assets/entities/crops/tomato2.png", texture_size),
            load_texture("assets/entities/crops/tomato3.png", texture_size),
            load_texture("assets/entities/crops/tomato4.png", texture_size),
        )
        super().__init__(code, pos, parent, textures, FPS * 60 * 5, "tomato_seeds", "tomato", 22)

    def drop_items(self):

        if self.growth_level >= len(self.texture) - 1:
            self.parent.drop_items(self.pos, self.item, randint(1, 2))
            for i in range(randint(2, 3)):
                self.parent.drop_items(self.pos, self.crop_item if randint(0, 9) else "rotten_tomato", 1)
        else:
            super().drop_items()
