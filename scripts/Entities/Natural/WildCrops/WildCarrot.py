from scripts.Entities.ABC.Building import Building
from scripts.Classes.Registry.EntityRegistry import EntityRegistry
from scripts.constants import *


TEXTURE_SIZE = TILE_SIZE * Vector(1, 1)
TEXTURE = load_texture("assets/entities/wild_carrot.png", TEXTURE_SIZE)
TEXTURE_OFFSET = TILE_SIZE * Vector(-0.5, -0.8)


class WildCarrot(Building, metaclass=EntityRegistry):

    def __init__(self, code, pos, parent):

        super().__init__(code, pos, parent, TEXTURE, 1, TEXTURE_OFFSET, "carrot_seeds", None, use_hibox=False)
