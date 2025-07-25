from scripts.constants import *
from scripts.Entities.ABC.Crop import Crop
from scripts.Classes.Registry.EntityRegistry import EntityRegistry


class Bamboo(Crop, metaclass=EntityRegistry):

    def __init__(self, code, pos, parent):

        texture_size = TILE_SIZE * Vector(1, 1.5)

        textures = (
            load_texture("assets/entities/crops/bamboo1.png", texture_size),
            load_texture("assets/entities/crops/bamboo2.png", texture_size),
            load_texture("assets/entities/crops/bamboo3.png", texture_size),
            load_texture("assets/entities/crops/bamboo4.png", texture_size),
        )
        super().__init__(code, pos, parent, textures, FPS * 60 * 3, "bamboo_seeds", "bamboo")
