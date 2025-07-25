from scripts.Entities.ABC.Building import Building
from scripts.Classes.Registry.EntityRegistry import EntityRegistry
from scripts.constants import *


TEXTURE_SIZE = TILE_SIZE * Vector(1, 1.5)
TEXTURE = load_texture("assets/entities/wild_wheat.png", TEXTURE_SIZE)
TEXTURE_OFFSET = TILE_SIZE * Vector(-0.5, -1.25)


class WildWheat(Building, metaclass=EntityRegistry):

    def __init__(self, code, pos, parent):

        super().__init__(code, pos, parent, TEXTURE, 1, TEXTURE_OFFSET, "wheat_seeds", None, use_hibox=False)
