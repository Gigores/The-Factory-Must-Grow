from scripts.constants import *
from scripts.Entities.ABC.Crop import Crop
from scripts.Classes.Registry.EntityRegistry import EntityRegistry


class CarrotCrop(Crop, metaclass=EntityRegistry):

    def __init__(self, code, pos, parent):

        texture_size = TILE_SIZE * Vector(1, 1.5)

        textures = (
            load_texture("assets/entities/crops/carrot1.png", texture_size),
            load_texture("assets/entities/crops/carrot2.png", texture_size),
            load_texture("assets/entities/crops/carrot3.png", texture_size),
            load_texture("assets/entities/crops/carrot4.png", texture_size),
        )
        super().__init__(code, pos, parent, textures, FPS * 60 * 5, "carrot_seeds", "carrot", 21)