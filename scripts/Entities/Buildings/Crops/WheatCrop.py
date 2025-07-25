from scripts.constants import *
from scripts.Entities.ABC.Crop import Crop
from random import randint
from scripts.Classes.Registry.EntityRegistry import EntityRegistry


class WheatCrop(Crop, metaclass=EntityRegistry):

    def __init__(self, code, pos, parent):

        texture_size = TILE_SIZE * Vector(1, 1.5)

        textures = (
            load_texture("assets/entities/crops/wheat1.png", texture_size),
            load_texture("assets/entities/crops/wheat2.png", texture_size),
            load_texture("assets/entities/crops/wheat3.png", texture_size),
            load_texture("assets/entities/crops/wheat4.png", texture_size),
        )
        super().__init__(code, pos, parent, textures, FPS * 60 * 5, "wheat_seeds", "wheat", 22)
