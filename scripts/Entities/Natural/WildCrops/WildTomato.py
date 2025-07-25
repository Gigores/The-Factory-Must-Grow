from scripts.Entities.ABC.Building import Building
from scripts.Classes.Registry.EntityRegistry import EntityRegistry
from scripts.constants import *


TEXTURE_SIZE = TILE_SIZE * Vector(1, 1)
TEXTURE = load_texture("assets/entities/wild_tomato.png", TEXTURE_SIZE)
TEXTURE_OFFSET = TILE_SIZE * Vector(-0.5, -0.6)


class WildTomato(Building, metaclass=EntityRegistry):

    def __init__(self, code, pos, parent):

        super().__init__(code, pos, parent, TEXTURE, 1, TEXTURE_OFFSET, "tomato_seeds", None, use_hibox=False)
